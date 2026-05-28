"""Job Matcher - Resume to Job Description Analysis

Analyzes resume content and matches it against Python job postings.
Provides match scores and recommendations.
"""

import sys
from pathlib import Path
from docx import Document
from collections import Counter
import re


# Sample job descriptions from Python Job Board
PYTHON_JOBS = [
    {
        "title": "Senior Back-End Python Engineer",
        "company": "ActivePrime, Inc.",
        "location": "REMOTE, WORLDWIDE",
        "type": "Back end",
        "requirements": [
            "Python", "backend development", "REST APIs", "databases",
            "microservices", "cloud platforms", "software architecture"
        ]
    },
    {
        "title": "Senior Fullstack Software Engineer",
        "company": "Autodesk",
        "location": "London, United Kingdom",
        "type": ["Back end", "Front end"],
        "requirements": [
            "Python", "JavaScript", "React", "backend", "frontend",
            "full stack", "REST APIs", "databases"
        ]
    },
    {
        "title": "Senior Python Engineer",
        "company": "Fulfil",
        "location": "Toronto, ON, Canada",
        "type": "Back end",
        "requirements": [
            "Python", "backend development", "Django", "Flask", "REST APIs",
            "software architecture", "databases"
        ]
    },
    {
        "title": "Python Developer",
        "company": "Ktek Resourcing",
        "location": "Columbus, Ohio, United States",
        "type": ["Back end", "Front end"],
        "requirements": [
            "Python", "JavaScript", "web development", "backend",
            "frontend", "databases"
        ]
    },
    {
        "title": "GenAI & Python Specialist",
        "company": "Deloitte",
        "location": "Toronto, Ontario, Canada",
        "type": ["Back end", "Cloud", "Machine Learning"],
        "requirements": [
            "Python", "machine learning", "AI", "cloud platforms",
            "backend development", "data processing"
        ]
    },
    {
        "title": "Machine Learning Engineer",
        "company": "Rebel Space Technologies",
        "location": "Long Beach, California, USA",
        "type": ["Back end", "Machine Learning", "Cloud"],
        "requirements": [
            "Python", "machine learning", "data science", "big data",
            "cloud platforms", "TensorFlow", "PyTorch"
        ]
    }
]


def extract_resume_content(file_path):
    """Extract text content from resume."""
    try:
        doc = Document(file_path)
        content = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                content.append(para.text.lower())
        
        return " ".join(content)
    except Exception as e:
        print(f"Error reading resume: {e}")
        return ""


def extract_skills(text):
    """Extract skills from text."""
    common_skills = [
        "python", "javascript", "sql", "django", "flask", "react",
        "rest api", "apis", "microservices", "cloud", "aws", "azure",
        "docker", "kubernetes", "git", "linux", "windows", "testing",
        "debugging", "databases", "mongodb", "postgresql", "mysql",
        "html", "css", "node.js", "express", "backend", "frontend",
        "fullstack", "web development", "devops", "ci/cd", "agile",
        "machine learning", "data science", "ai", "tensorflow", "pytorch"
    ]
    
    found_skills = []
    for skill in common_skills:
        if skill in text:
            found_skills.append(skill)
    
    return found_skills


def calculate_match_score(resume_skills, job_requirements):
    """Calculate match percentage between resume and job."""
    resume_skills_lower = [s.lower() for s in resume_skills]
    job_reqs_lower = [r.lower() for r in job_requirements]
    
    matches = sum(1 for req in job_reqs_lower if req in resume_skills_lower)
    total_requirements = len(job_reqs_lower)
    
    if total_requirements == 0:
        return 0
    
    return (matches / total_requirements) * 100


def analyze_resume_job_fit(resume_path):
    """Analyze how well resume fits various Python jobs."""
    
    # Extract resume content
    resume_content = extract_resume_content(resume_path)
    
    if not resume_content:
        print("Error: Could not extract resume content.")
        return
    
    # Extract skills from resume
    resume_skills = extract_skills(resume_content)
    
    print("\n" + "=" * 70)
    print("RESUME TO JOB MATCHER - ANALYSIS REPORT")
    print("=" * 70)
    
    print(f"\n📄 Resume File: {Path(resume_path).name}")
    print(f"\n🎯 Detected Skills in Resume:")
    if resume_skills:
        for skill in sorted(set(resume_skills)):
            print(f"   ✓ {skill.title()}")
    else:
        print("   No standard skills detected")
    
    # Match against jobs
    print(f"\n{'='*70}")
    print("JOB MATCHING RESULTS")
    print(f"{'='*70}\n")
    
    matches = []
    for job in PYTHON_JOBS:
        score = calculate_match_score(resume_skills, job["requirements"])
        matches.append({
            "job": job,
            "score": score,
            "matched_reqs": [req for req in job["requirements"] 
                           if req.lower() in resume_content]
        })
    
    # Sort by score (highest first)
    matches.sort(key=lambda x: x["score"], reverse=True)
    
    # Display results
    for idx, match in enumerate(matches, 1):
        job = match["job"]
        score = match["score"]
        
        # Color coding for score
        if score >= 70:
            status = "🟢 EXCELLENT FIT"
        elif score >= 50:
            status = "🟡 GOOD FIT"
        elif score >= 30:
            status = "🟠 MODERATE FIT"
        else:
            status = "🔴 LOW FIT"
        
        print(f"{idx}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Type: {job['type']}")
        print(f"   {status} ({score:.1f}%)")
        
        if match["matched_reqs"]:
            print(f"   Matched: {', '.join(set(match['matched_reqs']))}")
        
        # Show missing requirements
        missing = [req for req in job["requirements"] 
                  if req.lower() not in resume_content]
        if missing:
            print(f"   Missing: {', '.join(missing[:3])}")
        
        print()
    
    # Summary statistics
    print(f"{'='*70}")
    print("SUMMARY STATISTICS")
    print(f"{'='*70}")
    print(f"Total Jobs Analyzed: {len(PYTHON_JOBS)}")
    print(f"Average Match Score: {sum(m['score'] for m in matches) / len(matches):.1f}%")
    print(f"Best Match: {matches[0]['job']['title']} ({matches[0]['score']:.1f}%)")
    print(f"Worst Match: {matches[-1]['job']['title']} ({matches[-1]['score']:.1f}%)")
    
    # Recommendations
    print(f"\n{'='*70}")
    print("RECOMMENDATIONS FOR RESUME IMPROVEMENT")
    print(f"{'='*70}\n")
    
    # Find most common missing skills
    all_missing = []
    for match in matches:
        missing = [req for req in match["job"]["requirements"] 
                  if req.lower() not in resume_content]
        all_missing.extend(missing)
    
    if all_missing:
        missing_counter = Counter(all_missing)
        print("Top skills to add to resume:")
        for skill, count in missing_counter.most_common(5):
            print(f"  • {skill} (appears in {count} job postings)")
    
    print(f"\n{'='*70}\n")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python job_matcher.py <path_to_resume.docx>")
        print("\nExample: python job_matcher.py resumes/sample_resume.docx")
        sys.exit(1)
    
    resume_path = sys.argv[1]
    analyze_resume_job_fit(resume_path)


if __name__ == "__main__":
    main()
