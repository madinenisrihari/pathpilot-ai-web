"""
Fallback roadmap generator using hardcoded templates.

This is the original logic PathPilot AI used before Gemini was wired up
for real. It's kept as a safety net so the API still returns a usable
roadmap if GEMINI_API_KEY is missing or the Gemini call fails.
"""

CAREER_DOMAINS = {
    "data science": {
        "topics": [
            "Python Fundamentals & Jupyter Setup",
            "NumPy & Pandas for Data Manipulation",
            "Data Cleaning & Exploratory Data Analysis",
            "Data Visualization with Matplotlib & Seaborn",
            "Statistics & Probability Foundations",
            "Machine Learning Basics — Supervised Learning",
            "Regression & Classification Models",
            "Unsupervised Learning & Clustering",
            "Feature Engineering & Model Evaluation",
            "Introduction to Deep Learning with TensorFlow",
            "Natural Language Processing Basics",
            "Capstone: End-to-End Data Science Project",
        ],
        "resources": [
            ["Kaggle Learn — Python", "https://www.kaggle.com/learn/python"],
            ["freeCodeCamp — Python for Everybody", "https://www.freecodecamp.org/learn/scientific-computing-with-python/"],
            ["Kaggle Learn — Pandas", "https://www.kaggle.com/learn/pandas"],
            ["Kaggle Learn — Data Visualization", "https://www.kaggle.com/learn/data-visualization"],
            ["StatQuest YouTube Channel", "https://www.youtube.com/c/joshstarmer"],
            ["Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"],
            ["scikit-learn Documentation", "https://scikit-learn.org/stable/user_guide.html"],
            ["fast.ai — Practical Deep Learning", "https://course.fast.ai/"],
            ["TensorFlow Tutorials", "https://www.tensorflow.org/tutorials"],
            ["Hugging Face NLP Course", "https://huggingface.co/learn/nlp-course/chapter1/1"],
            ["fast.ai NLP", "https://course.fast.ai/"],
            ["Kaggle Competitions", "https://www.kaggle.com/competitions"],
        ],
        "projects": [
            "Analyze a CSV dataset and write a summary report",
            "Build a data cleaning pipeline for messy real-world data",
            "Create an interactive EDA dashboard with Plotly",
            "Visualize COVID-19 trends with Matplotlib & Seaborn",
            "Run A/B test analysis on sample e-commerce data",
            "Predict house prices with linear regression",
            "Build a spam email classifier with scikit-learn",
            "Customer segmentation using K-Means clustering",
            "Feature engineering challenge on the Titanic dataset",
            "Train a neural network on MNIST digits",
            "Sentiment analysis on movie reviews",
            "Full portfolio project: predict churn for a SaaS company",
        ],
    },
    "web development": {
        "topics": [
            "HTML5 & Semantic Web Structure",
            "CSS3, Flexbox & Responsive Design",
            "JavaScript Fundamentals & DOM Manipulation",
            "Git, GitHub & Developer Workflow",
            "Advanced JavaScript — ES6+ & Async/Await",
            "React.js — Components, Props & State",
            "React Hooks, Routing & State Management",
            "Node.js & Express — Building REST APIs",
            "Databases — SQL Basics & MongoDB",
            "Authentication, Security & Deployment",
            "Full-Stack Integration & Testing",
            "Capstone: Deploy a Full-Stack Web Application",
        ],
        "resources": [
            ["MDN Web Docs — HTML", "https://developer.mozilla.org/en-US/docs/Web/HTML"],
            ["freeCodeCamp — Responsive Web Design", "https://www.freecodecamp.org/learn/2022/responsive-web-design/"],
            ["JavaScript.info", "https://javascript.info/"],
            ["GitHub Skills", "https://skills.github.com/"],
            ["freeCodeCamp — JavaScript Algorithms", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"],
            ["React Official Docs", "https://react.dev/learn"],
            ["React Router Docs", "https://reactrouter.com/en/main"],
            ["Node.js Getting Started Guide", "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs"],
            ["SQLBolt — Interactive SQL Tutorial", "https://sqlbolt.com/"],
            ["OWASP Web Security Basics", "https://owasp.org/www-project-web-security-testing-guide/"],
            ["Jest Testing Framework Docs", "https://jestjs.io/docs/getting-started"],
            ["Vercel Deployment Guide", "https://vercel.com/docs"],
        ],
        "projects": [
            "Build a personal portfolio landing page",
            "Create a responsive photo gallery with CSS Grid",
            "Todo app with local storage persistence",
            "Contribute your first pull request on GitHub",
            "Weather app using a free public API",
            "Component library with reusable React components",
            "Blog app with React Router and markdown support",
            "REST API for a book library with Express",
            "CRUD app connected to a SQLite database",
            "Add JWT authentication to your API",
            "Write unit tests for your React components",
            "Deploy a full-stack MERN app to the cloud",
        ],
    },
    "machine learning": {
        "topics": [
            "Python & Math Refresher for ML",
            "Linear Algebra & Calculus Essentials",
            "Data Preprocessing & Feature Scaling",
            "Supervised Learning — Linear Models",
            "Decision Trees & Ensemble Methods",
            "Model Selection & Cross-Validation",
            "Unsupervised Learning — PCA & Clustering",
            "Neural Networks from Scratch",
            "Deep Learning with PyTorch",
            "Computer Vision Fundamentals",
            "MLOps — Model Deployment & Monitoring",
            "Capstone: Production-Ready ML Pipeline",
        ],
        "resources": [
            ["3Blue1Brown — Linear Algebra", "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab"],
            ["Khan Academy — Calculus", "https://www.khanacademy.org/math/calculus-1"],
            ["scikit-learn Preprocessing Guide", "https://scikit-learn.org/stable/modules/preprocessing.html"],
            ["Andrew Ng — ML Specialization (audit free)", "https://www.coursera.org/specializations/machine-learning-introduction"],
            ["StatQuest — Random Forests", "https://www.youtube.com/watch?v=J4Wdy0nx_c8"],
            ["scikit-learn Model Selection", "https://scikit-learn.org/stable/model_selection.html"],
            ["Google ML Clustering Course", "https://developers.google.com/machine-learning/clustering"],
            ["Neural Networks and Deep Learning (book)", "http://neuralnetworksanddeeplearning.com/"],
            ["PyTorch Official Tutorials", "https://pytorch.org/tutorials/"],
            ["fast.ai — Practical Deep Learning", "https://course.fast.ai/"],
            ["Made With ML — MLOps Guide", "https://madewithml.com/"],
            ["Hugging Face Model Hub", "https://huggingface.co/models"],
        ],
        "projects": [
            "Implement gradient descent from scratch in NumPy",
            "Predict student grades with linear regression",
            "Build a random forest classifier for iris flowers",
            "Hyperparameter tuning with GridSearchCV",
            "Customer segmentation with K-Means on retail data",
            "Build a 2-layer neural network without frameworks",
            "Image classifier on CIFAR-10 with PyTorch",
            "Object detection demo with a pre-trained model",
            "Deploy a model as a FastAPI microservice",
            "Build an end-to-end ML pipeline with MLflow",
            "Create a model monitoring dashboard",
            "Capstone: train, deploy, and monitor a real-world model",
        ],
    },
    "cybersecurity": {
        "topics": [
            "Networking Fundamentals & OSI Model",
            "Linux Command Line & Shell Scripting",
            "Cryptography Basics & Hashing",
            "Web Application Security & OWASP Top 10",
            "Network Scanning & Reconnaissance",
            "Vulnerability Assessment & Penetration Testing",
            "Security Operations & SIEM Tools",
            "Cloud Security Fundamentals",
            "Incident Response & Forensics",
            "Identity & Access Management",
            "Security Automation & Scripting",
            "Capstone: Security Audit & Report",
        ],
        "resources": [
            ["Professor Messer — Network+", "https://www.professormesser.com/network-plus/n10-008/n10-008-video-playlist/"],
            ["OverTheWire — Bandit Linux Wargame", "https://overthewire.org/wargames/bandit/"],
            ["Crypto101 — Free Book", "https://www.crypto101.io/"],
            ["OWASP WebGoat", "https://owasp.org/www-project-webgoat/"],
            ["TryHackMe — Free Rooms", "https://tryhackme.com/"],
            ["HackTheBox — Starting Point", "https://www.hackthebox.com/"],
            ["Splunk Boss of the SOC", "https://www.splunk.com/en_us/blog/security/boss-of-the-soc.html"],
            ["AWS Cloud Security Fundamentals", "https://aws.amazon.com/training/digital/aws-cloud-security-fundamentals/"],
            ["SANS Digital Forensics Poster", "https://www.sans.org/posters/digital-forensics-and-incident-response/"],
            ["IAM Best Practices — AWS", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html"],
            ["Automate the Boring Stuff — Python", "https://automatetheboringstuff.com/"],
            ["NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework"],
        ],
        "projects": [
            "Set up a home lab with VirtualBox & Kali Linux",
            "Write a Bash script to audit open ports",
            "Implement Caesar cipher & SHA-256 hasher in Python",
            "Find and fix XSS vulnerabilities in WebGoat",
            "Perform a network scan report with Nmap",
            "Complete 5 TryHackMe beginner rooms",
            "Build a simple SIEM alert dashboard",
            "Configure AWS IAM roles with least privilege",
            "Analyze a PCAP file for suspicious traffic",
            "Design an RBAC policy for a small company",
            "Automate vulnerability scanning with Python",
            "Write a full security audit report for a web app",
        ],
    },
    "cloud computing": {
        "topics": [
            "Cloud Concepts & Service Models (IaaS/PaaS/SaaS)",
            "AWS Core Services — EC2, S3, IAM",
            "Networking — VPC, Subnets & Security Groups",
            "Databases in the Cloud — RDS & DynamoDB",
            "Containers & Docker Fundamentals",
            "Kubernetes Basics & Orchestration",
            "Serverless Computing with AWS Lambda",
            "Infrastructure as Code — Terraform",
            "CI/CD Pipelines & DevOps Practices",
            "Cloud Monitoring, Logging & Cost Optimization",
            "Multi-Cloud & Hybrid Cloud Strategies",
            "Capstone: Deploy a Scalable Cloud Architecture",
        ],
        "resources": [
            ["AWS Cloud Practitioner Essentials (free)", "https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials"],
            ["AWS EC2 Getting Started", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html"],
            ["AWS VPC Documentation", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html"],
            ["AWS RDS User Guide", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html"],
            ["Docker Getting Started", "https://docs.docker.com/get-started/"],
            ["Kubernetes Basics — Interactive Tutorial", "https://kubernetes.io/docs/tutorials/kubernetes-basics/"],
            ["AWS Lambda Developer Guide", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html"],
            ["Terraform Learn — AWS", "https://developer.hashicorp.com/terraform/tutorials/aws-get-started"],
            ["GitHub Actions Docs", "https://docs.github.com/en/actions"],
            ["AWS CloudWatch Docs", "https://docs.aws.amazon.com/cloudwatch/"],
            ["Google Cloud Skills Boost — Free Tier", "https://www.cloudskillsboost.google/"],
            ["AWS Well-Architected Framework", "https://aws.amazon.com/architecture/well-architected/"],
        ],
        "projects": [
            "Launch and secure your first EC2 instance",
            "Build a static website hosted on S3",
            "Design a VPC with public & private subnets",
            "Deploy a PostgreSQL database on RDS",
            "Containerize a Python app with Docker",
            "Deploy a microservice to a Kubernetes cluster",
            "Build a serverless REST API with API Gateway + Lambda",
            "Provision AWS infrastructure with Terraform",
            "Set up a CI/CD pipeline with GitHub Actions",
            "Create CloudWatch alarms and a cost budget",
            "Compare AWS vs Azure pricing for a sample workload",
            "Design and document a 3-tier cloud architecture",
        ],
    },
}

DEFAULT_DOMAIN = {
    "topics": [
        "Goal Setting & Learning Mindset",
        "Core Concepts & Terminology",
        "Essential Tools & Environment Setup",
        "Foundational Skills — Part 1",
        "Foundational Skills — Part 2",
        "Intermediate Concepts & Patterns",
        "Hands-On Practice & Problem Solving",
        "Advanced Techniques & Best Practices",
        "Industry Standards & Frameworks",
        "Soft Skills & Professional Development",
        "Portfolio Building & Networking",
        "Capstone Project & Career Next Steps",
    ],
    "resources": [
        ["Coursera — Free Audit Courses", "https://www.coursera.org/"],
        ["edX — Free Courses", "https://www.edx.org/"],
        ["YouTube — freeCodeCamp", "https://www.youtube.com/c/Freecodecamp"],
        ["Khan Academy", "https://www.khanacademy.org/"],
        ["MIT OpenCourseWare", "https://ocw.mit.edu/"],
        ["Udemy Free Courses", "https://www.udemy.com/courses/free/"],
        ["LinkedIn Learning (library access)", "https://www.linkedin.com/learning/"],
        ["GitHub Learning Lab", "https://lab.github.com/"],
        ["Medium — Free Articles", "https://medium.com/"],
        ["Reddit Learning Communities", "https://www.reddit.com/r/learnprogramming/"],
        ["Dev.to — Developer Blog", "https://dev.to/"],
        ["Portfolio Inspiration — Behance", "https://www.behance.net/"],
    ],
    "projects": [
        "Write a personal learning manifesto and 12-week plan",
        "Create flashcards for 50 key terms in your field",
        "Set up your development/study environment",
        "Complete 10 practice exercises on core concepts",
        "Build a cheat sheet document for quick reference",
        "Solve 5 real-world scenario problems",
        "Complete a 48-hour mini hackathon project",
        "Write a technical blog post explaining a concept",
        "Contribute to an open-source project (good first issue)",
        "Mock interview practice with a peer or AI",
        "Build a portfolio website showcasing your work",
        "Present your capstone project in a demo video",
    ],
}

SKILL_MODIFIERS = {
    "Beginner": {"prefix": "Foundations: ", "hours_factor": 1.0},
    "Intermediate": {"prefix": "", "hours_factor": 0.85},
    "Advanced": {"prefix": "Advanced: ", "hours_factor": 0.7},
}


def detect_domain(career_goal: str) -> dict:
    goal_lower = career_goal.lower()
    for keyword, domain in CAREER_DOMAINS.items():
        if keyword in goal_lower:
            return domain
    for keyword, domain in CAREER_DOMAINS.items():
        words = keyword.split()
        if any(word in goal_lower for word in words):
            return domain
    return DEFAULT_DOMAIN


def generate_template_roadmap(career_goal: str, skill_level: str, hours_per_day: float) -> list[dict]:
    """Deterministic, offline fallback roadmap generator (no AI call)."""
    domain = detect_domain(career_goal)
    modifier = SKILL_MODIFIERS[skill_level]
    weekly_hours = round(hours_per_day * 7 * modifier["hours_factor"], 1)

    weeks = []
    for i in range(12):
        topic = domain["topics"][i]
        if skill_level == "Beginner" and i < 4:
            topic = modifier["prefix"] + topic
        elif skill_level == "Advanced" and i >= 8:
            topic = modifier["prefix"] + topic

        resource_name, resource_url = domain["resources"][i]
        weeks.append({
            "week": i + 1,
            "topic": topic,
            "resource_name": resource_name,
            "resource_url": resource_url,
            "project": domain["projects"][i],
            "hours": weekly_hours,
        })
    return weeks
