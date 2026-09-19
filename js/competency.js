const Competency = {
  data: [],

  init: async function() {
    try {
      this.data = await window.api.get('/trainees/me/competencies');
      this.renderCompetencyTable();
      this.updateCounters();
    } catch (error) {
      console.error('Failed to load competencies:', error);
      const tbody = document.getElementById('competency-table-body');
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" style="padding: var(--spacing-md); text-align: center;">
              Failed to load competencies.
            </td>
          </tr>
        `;
      }
    }
  },

  formatStatus: function(status) {
    return status
      .toLowerCase()
      .replace(/_/g, ' ')
      .replace(/\b\w/g, char => char.toUpperCase());
  },

  getStatusClass: function(status) {
    if (status === 'VERIFIED') return 'badge-success';
    if (status === 'ASSESSED') return 'badge-warning';
    if (status === 'LEARNING' || status === 'AI_ESTIMATED') return 'badge-ai';
    return 'badge-danger';
  },

  renderCompetencyTable: function() {
    const tbody = document.getElementById('competency-table-body');
    if (!tbody) return;

    let html = '';

    this.data.forEach(comp => {
      const progress = Math.min(
        100,
        Math.max(0, (comp.proficiency_level / 5) * 100)
      );

      const status = this.formatStatus(comp.verification_status);
      const statusBadgeClass = this.getStatusClass(comp.verification_status);

      html += `
        <tr style="border-bottom: 1px solid var(--border-default);">
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-weight: 600; color: var(--color-primary);">
            ${comp.name}
          </td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">
            ${comp.level}
          </td>
          <td style="padding: var(--spacing-md) var(--spacing-sm); font-size: var(--text-sm);">
            ${comp.category || '—'}
          </td>
          <td style="padding: var(--spacing-md) var(--spacing-sm);">
            <div class="progress-container" style="width: 100px;">
              <div class="progress-bar ${progress >= 80 ? 'success' : ''}" style="width: ${progress}%"></div>
            </div>
          </td>
          <td style="padding: var(--spacing-md) var(--spacing-sm);">
            <span class="badge ${statusBadgeClass}">${status}</span>
          </td>
        </tr>
      `;
    });

    if (!this.data.length) {
      html = `
        <tr>
          <td colspan="5" style="padding: var(--spacing-md); text-align: center;">
            No competencies found.
          </td>
        </tr>
      `;
    }

    tbody.innerHTML = html;
  },

  updateCounters: function() {
    const vCount = document.getElementById('comp-verified-count');
    const aCount = document.getElementById('comp-assessed-count');
    const uCount = document.getElementById('comp-unverified-count');

    const verified = this.data.filter(
      comp => comp.verification_status === 'VERIFIED'
    ).length;

    const assessed = this.data.filter(
      comp => comp.verification_status === 'ASSESSED'
    ).length;

    const unverified = this.data.filter(
      comp =>
        comp.verification_status !== 'VERIFIED' &&
        comp.verification_status !== 'ASSESSED'
    ).length;

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