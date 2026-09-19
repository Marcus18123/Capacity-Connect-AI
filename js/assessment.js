const Assessment = {
  data: [],
  currentAssessment: null,
  userAnswers: {},

  init: async function() {
    await this.fetchAssessments();
  },

  fetchAssessments: async function() {
    const container = document.getElementById('assessment-list');
    if (!container) return;

    try {
      this.data = await window.api.get('/assessments/');
      this.renderAssessmentsList();
    } catch (e) {
      console.error("Failed to load assessments", e);
      container.innerHTML = `<div class="p-md text-center text-muted">Failed to load assessments.</div>`;
    }
  },

  renderAssessmentsList: function() {
    const container = document.getElementById('assessment-list');
    if (!container) return;

    if (!this.data || !this.data.length) {
      container.innerHTML = `<div class="p-md text-center text-muted">No assessments currently available.</div>`;
      return;
    }

    let html = '';
    this.data.forEach(a => {
      let statusBadge = '';
      let scoreHtml = '';
      
      if (a.passed) {
        statusBadge = `<span class="badge badge-success">Passed</span>`;
        scoreHtml = `<div class="font-weight-bold text-success" style="font-size: var(--text-lg);">${a.last_score} pts</div>`;
      } else if (a.status === 'TAKEN') {
        statusBadge = `<span class="badge badge-warning">Retake Needed</span>`;
        scoreHtml = `<button class="btn btn-primary btn-sm" onclick="Assessment.startAssessment('${a.id}')">Try Again</button>`;
      } else {
        statusBadge = `<span class="badge badge-ai">Available</span>`;
        scoreHtml = `<button class="btn btn-primary btn-sm" onclick="Assessment.startAssessment('${a.id}')">Start Assessment</button>`;
      }

      html += `
        <div style="border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: var(--spacing-md); display: flex; justify-content: space-between; align-items: center;">
          <div>
            <div class="flex gap-sm items-center mb-xs">
              <h4 style="color: var(--color-primary); margin: 0;">${a.title}</h4>
              ${statusBadge}
            </div>
            <div class="text-xs text-muted mb-xs">${a.description || 'Competency assessment quiz.'}</div>
            <div class="text-xs text-muted"><strong class="text-neutral">Questions:</strong> ${a.question_count} | <strong class="text-neutral">Passing Score:</strong> ${a.passing_score}%</div>
          </div>
          <div style="text-align: right;">
            ${scoreHtml}
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  startAssessment: async function(assessmentId) {
    const container = document.getElementById('active-assessment-container');
    if (!container) return;

    try {
      this.currentAssessment = await window.api.get(`/assessments/${assessmentId}/questions`);
      this.userAnswers = {};
      this.renderQuizUI();
    } catch (e) {
      alert("Error starting assessment: " + e.message);
    }
  },

  renderQuizUI: function() {
    const container = document.getElementById('active-assessment-container');
    if (!container || !this.currentAssessment) return;

    const questions = this.currentAssessment.questions || [];
    if (!questions.length) {
      container.innerHTML = `<div class="p-md text-center text-muted">No questions found for this assessment.</div>`;
      return;
    }

    let html = `
      <div class="card card-ai">
        <span class="badge badge-ai mb-sm">✨ Active Assessment</span>
        <h3 class="card-title mb-xs">${this.currentAssessment.title}</h3>
        <p class="text-xs text-muted mb-md">${this.currentAssessment.description}</p>
    `;

    questions.forEach((q, idx) => {
      html += `
        <div class="mb-lg p-sm" style="background: white; border-radius: var(--radius-sm); border: 1px solid var(--border-default);">
          <div class="mb-sm" style="font-size: var(--text-sm); font-weight: 600;">
            Question ${idx + 1}: ${q.question_text}
          </div>
          <div class="flex-col gap-sm">
      `;

      (q.options || []).forEach(opt => {
        html += `
          <label style="display: flex; gap: var(--spacing-sm); align-items: center; padding: var(--spacing-xs) var(--spacing-sm); border: 1px solid var(--border-default); border-radius: var(--radius-sm); cursor: pointer;">
            <input type="radio" name="q_${q.id}" value="${opt}" onchange="Assessment.userAnswers['${q.id}'] = '${opt}'">
            <span class="text-sm">${opt}</span>
          </label>
        `;
      });

      html += `
          </div>
        </div>
      `;
    });

    html += `
        <div class="flex justify-between items-center mt-md">
          <button class="btn btn-outline" onclick="Assessment.cancelQuiz()">Cancel</button>
          <button class="btn btn-primary" onclick="Assessment.submitQuiz()">Submit Assessment</button>
        </div>
      </div>
    `;

    container.innerHTML = html;
  },

  cancelQuiz: function() {
    const container = document.getElementById('active-assessment-container');
    if (container) container.innerHTML = '';
    this.currentAssessment = null;
  },

  submitQuiz: async function() {
    if (!this.currentAssessment) return;

    const answersPayload = Object.keys(this.userAnswers).map(qId => ({
      question_id: qId,
      selected_option: this.userAnswers[qId]
    }));

    try {
      const res = await window.api.post(`/assessments/${this.currentAssessment.assessment_id}/submit`, {
        answers: answersPayload
      });

      alert(`${res.message}\nScore: ${res.score}/${res.total_marks} (${res.percentage}%)`);
      this.cancelQuiz();
      await this.fetchAssessments();
    } catch (e) {
      alert("Submission error: " + e.message);
    }
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('assessment-list')) {
    Assessment.init();
  }
});
