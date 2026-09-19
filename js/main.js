/**
 * CAPACITY CONNECT AI - Main JavaScript & Shared Utilities
 */

// ==========================================================================
// MOCK DATA LAYER (Prepared for Phase 2 API replacement)
// ==========================================================================
const mockData = {
  user: {
    name: "Elena Rostova",
    role: "Senior AI Solutions Architect Trainee",
    organization: "Global Tech Group",
    avatarUrl: "",
    competencyIndex: 84.2,
    activeLearningHours: 32.5,
    targetHours: 40,
    skillGapsCount: 3,
    verifiedCompetenciesCount: 18
  },
  
  competencies: [
    { name: "Python", level: "Advanced", target: "Advanced", status: "Verified", progress: 95 },
    { name: "SQL", level: "Intermediate", target: "Advanced", status: "Verified", progress: 85 },
    { name: "Statistics", level: "Intermediate", target: "Advanced", status: "Assessed", progress: 75 },
    { name: "Machine Learning", level: "Intermediate", target: "Advanced", status: "Learning", progress: 60 },
    { name: "GIS", level: "Beginner", target: "Intermediate", status: "Unverified", progress: 30 },
    { name: "Multi-Agent Systems", level: "Intermediate", target: "Advanced", status: "Gap", progress: 64 },
    { name: "LLM Fine-Tuning", level: "Advanced", target: "Advanced", status: "Verified", progress: 92 },
    { name: "RAG Architecture", level: "Advanced", target: "Advanced", status: "Verified", progress: 88 }
  ],
  
  skillGaps: [
    { 
      id: 1, 
      competency: "Autonomous Multi-Agent Swarms", 
      priority: "HIGH", 
      impact: "+18% to Benchmark",
      targetDate: "Aug 18",
      modulesRequired: 2,
      current: 40,
      target: 85
    },
    { 
      id: 2, 
      competency: "Latency Optimization for Local SLMs", 
      priority: "MEDIUM", 
      impact: "+9% to Benchmark",
      targetDate: "Sep 02",
      modulesRequired: 1,
      current: 55,
      target: 80
    },
    { 
      id: 3, 
      competency: "EU AI Act Compliance", 
      priority: "MEDIUM", 
      impact: "+7% to Benchmark",
      targetDate: "Sep 15",
      modulesRequired: 1,
      current: 20,
      target: 70
    }
  ],
  
  learningPath: {
    track: "Production LLM Systems & Agentic Workflows",
    progress: 68,
    modulesCompleted: 6,
    modulesTotal: 9,
    steps: [
      { title: "Semantic Caching & Vector DB Optimization", status: "Completed", type: "Course" },
      { title: "Guardrails & Prompt Injection Mitigation", status: "In Progress", type: "Course" },
      { title: "Autonomous Multi-Agent Swarms", status: "Upcoming", type: "Course" },
      { title: "Applied Agentic Project", status: "Upcoming", type: "Project" }
    ]
  },
  
  trainers: [
    {
      id: 1,
      name: "Aura - Senior AI Architecture Mentor",
      expertise: "Time-Series Forecasting, Python-based analytics",
      experience: "8 years",
      matchScore: 94,
      availability: "Online & Context-Aware"
    },
    {
      id: 2,
      name: "Dr. Marcus Chen",
      expertise: "Machine Learning, LLM Fine-Tuning",
      experience: "12 years",
      matchScore: 88,
      availability: "Available next week"
    }
  ],

  recentActivity: [
    { title: "Assessment completed", detail: "Advanced Statistics", score: "82%", type: "assessment" },
    { title: "Course completed", detail: "Data Visualization", score: "", type: "course" },
    { title: "Competency verified", detail: "Python", score: "", type: "verification" }
  ]
};

// ==========================================================================
// SHARED UTILITIES
// ==========================================================================

const AppUtils = {
  /**
   * Initializes common UI elements like sidebar toggling
   */
  initShell: function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (menuToggle && sidebar) {
      menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
      });
      
      // Close sidebar when clicking outside on mobile
      document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
          if (!sidebar.contains(e.target) && !menuToggle.contains(e.target) && sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
          }
        }
      });
    }

    // Load User Profile in Topbar
    this.populateUserShell();
  },

  /**
   * Populates user details in the topbar if elements exist
   */
  populateUserShell: function() {
    // We try to get user from localStorage to see if someone is logged in
    const storedUser = localStorage.getItem('capacity_user');
    let userToDisplay = mockData.user;

    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        userToDisplay.name = parsed.name || userToDisplay.name;
        userToDisplay.role = parsed.role === 'admin' ? 'Administrator' : 
                             parsed.role === 'trainer' ? 'Trainer' : 
                             'Senior AI Solutions Architect Trainee';
      } catch(e) {}
    }

    const userNameEl = document.getElementById('topbar-user-name');
    const userRoleEl = document.getElementById('topbar-user-role');
    const avatarEl = document.getElementById('topbar-user-avatar');

    if (userNameEl) userNameEl.textContent = userToDisplay.name;
    if (userRoleEl) userRoleEl.textContent = userToDisplay.role;
    if (avatarEl) {
      // Create initials
      const initials = userToDisplay.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
      avatarEl.textContent = initials;
    }
  },

  /**
   * Creates a simple DOM element with classes and text
   */
  createElement: function(tag, className, textContent) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (textContent) el.textContent = textContent;
    return el;
  },

  /**
   * Helper to determine priority badge classes
   */
  getPriorityClass: function(priority) {
    switch(priority.toUpperCase()) {
      case 'HIGH': return 'badge-danger';
      case 'MEDIUM': return 'badge-warning';
      case 'LOW': return 'badge-success';
      default: return 'badge-success';
    }
  }
};

// Initialize on DOM Load
document.addEventListener('DOMContentLoaded', () => {
  AppUtils.initShell();
});
