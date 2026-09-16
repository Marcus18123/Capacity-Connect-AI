/**
 * CAPACITY CONNECT AI - Assessment Logic
 */

const Assessment = {
  init: function() {
    this.renderAssessments();
  },

  renderAssessments: function() {
    const container = document.getElementById('assessment-list');
    if (!container) return;

    const list = [
      { 
        name: "LangGraph Architecture Basics", 
        course: "Multi-Agent Swarms",
        competencies: "Multi-Agent Systems",
        questions: 15,
        deadline: "Aug 15",
        status: "Upcoming"
      },
      { 
        name: "Advanced Statistics", 
        course: "Statistics Fundamentals",
        competencies: "Statistics",
        questions: 20,
        deadline: "Completed",
        status: "Completed",
        score: "82%"
      },
      { 
        name: "Data Visualization Best Practices", 
        course: "Data Visualization",
        competencies: "Data Analysis",
        questions: 10,
        deadline: "Completed",
        status: "Completed",
        score: "89%"
      }
    ];

    let html = '';
    list.forEach(a => {
      let statusBadge = '';
      let scoreHtml = '';
      
      if (a.status === 'Completed') {
        statusBadge = `<span class="badge badge-success">Completed</span>`;
        scoreHtml = `<div class="font-weight-bold text-success" style="font-size: var(--text-lg);">${a.score}</div>`;
      } else {
        statusBadge = `<span class="badge badge-warning">Upcoming</span>`;
        scoreHtml = `<button class="btn btn-primary btn-sm" style="padding: 0.25rem 0.5rem; font-size: var(--text-xs);">Start Now</button>`;
      }

      html += `
        <div style="border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: var(--spacing-md); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div class="flex gap-sm items-center mb-xs">
              <h4 style="color: var(--color-primary); margin: 0;">${a.name}</h4>
              ${statusBadge}
            </div>
            <div class="text-xs text-muted mb-xs"><strong class="text-neutral">Course:</strong> ${a.course}</div>
            <div class="text-xs text-muted mb-xs"><strong class="text-neutral">Competency:</strong> ${a.competencies}</div>
            <div class="text-xs text-muted"><strong class="text-neutral">Questions:</strong> ${a.questions} | <strong class="text-neutral">Deadline:</strong> ${a.deadline}</div>
          </div>
          <div style="text-align: right;">
            ${scoreHtml}
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('assessment-list')) {
    Assessment.init();
  }
});
