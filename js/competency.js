/**
 * CAPACITY CONNECT AI - Competency Logic
 */

const Competency = {
  init: function() {
    this.renderCompetencyTable();
    this.updateCounters();
  },

  renderCompetencyTable: function() {
    const tbody = document.getElementById('competency-table-body');
    if (!tbody) return;

    let html = '';
    mockData.competencies.forEach(comp => {
      
      let statusBadgeClass = 'badge-danger'; // default unverified/gap
      if (comp.status === 'Verified') statusBadgeClass = 'badge-success';
      if (comp.status === 'Assessed') statusBadgeClass = 'badge-warning';
      if (comp.status === 'Learning') statusBadgeClass = 'badge-ai';

      html += `
        <tr style="border-bottom: 1px solid var(--border-default);">
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-weight: 600; color: var(--color-primary);">${comp.name}</td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">${comp.level}</td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">${comp.target}</td>
          <td style="padding: var(--spacing-md) var(--spacing-sm);">
            <div class="progress-container" style="width: 100px;">
              <div class="progress-bar ${comp.progress >= 80 ? 'success' : ''}" style="width: ${comp.progress}%"></div>
            </div>
          </td>
          <td style="padding: var(--spacing-md) var(--spacing-sm);">
            <span class="badge ${statusBadgeClass}">${comp.status}</span>
          </td>
        </tr>
      `;
    });

    tbody.innerHTML = html;
  },

  updateCounters: function() {
    const vCount = document.getElementById('comp-verified-count');
    const aCount = document.getElementById('comp-assessed-count');
    const uCount = document.getElementById('comp-unverified-count');

    let verified = 0, assessed = 0, unverified = 0;

    mockData.competencies.forEach(comp => {
      if (comp.status === 'Verified') verified++;
      else if (comp.status === 'Assessed') assessed++;
      else unverified++;
    });

    if (vCount) vCount.textContent = verified;
    if (aCount) aCount.textContent = assessed;
    if (uCount) uCount.textContent = unverified;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('competency-table-body')) {
    Competency.init();
  }
});
