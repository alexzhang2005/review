/* ===== Daily Review App ===== */
(function () {
  'use strict';

  /* ---------- Constants ---------- */
  const STORAGE_KEY = 'daily_reviews';
  const MOOD_MAP = {
    1: { emoji: '😞', label: '很糟糕' },
    2: { emoji: '😕', label: '一般' },
    3: { emoji: '😐', label: '还好' },
    4: { emoji: '😊', label: '不错' },
    5: { emoji: '🤩', label: '非常好' },
  };

  /* ---------- State ---------- */
  let reviews = loadReviews();
  let editingId = null;
  let deletingId = null;

  /* ---------- DOM refs ---------- */
  const form          = document.getElementById('reviewForm');
  const formSection   = document.getElementById('formSection');
  const toggleFormBtn = document.getElementById('toggleFormBtn');
  const formTitle     = document.getElementById('formTitle');
  const cancelBtn     = document.getElementById('cancelBtn');
  const submitBtn     = document.getElementById('submitBtn');
  const reviewList    = document.getElementById('reviewList');
  const emptyState    = document.getElementById('emptyState');
  const searchInput   = document.getElementById('searchInput');
  const sortSelect    = document.getElementById('sortSelect');

  const deleteModal      = document.getElementById('deleteModal');
  const cancelDeleteBtn  = document.getElementById('cancelDeleteBtn');
  const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

  const detailModal       = document.getElementById('detailModal');
  const detailDate        = document.getElementById('detailDate');
  const detailContent     = document.getElementById('detailContent');
  const closeDetailBtn    = document.getElementById('closeDetailBtn');
  const closeDetailBtn2   = document.getElementById('closeDetailBtn2');
  const editFromDetailBtn = document.getElementById('editFromDetailBtn');

  /* ---------- Init ---------- */
  setTodayDate();
  renderList();

  /* ---------- Storage ---------- */
  function loadReviews() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch {
      return [];
    }
  }

  function saveReviews() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(reviews));
  }

  /* ---------- Helpers ---------- */
  function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2);
  }

  function setTodayDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('reviewDate').value = today;
  }

  function formatDate(dateStr) {
    const [year, month, day] = dateStr.split('-');
    const d = new Date(dateStr + 'T00:00:00');
    const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
    return `${year}年${month}月${day}日 周${weekdays[d.getDay()]}`;
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str || ''));
    return div.innerHTML;
  }

  function showToast(message, type = '') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2800);
  }

  /* ---------- Form ---------- */
  function getFormData() {
    const mood = form.querySelector('input[name="mood"]:checked');
    return {
      date:         form.reviewDate.value,
      achievements: form.achievements.value.trim(),
      problems:     form.problems.value.trim(),
      learnings:    form.learnings.value.trim(),
      tomorrow:     form.tomorrow.value.trim(),
      mood:         mood ? Number(mood.value) : null,
    };
  }

  function populateForm(review) {
    form.reviewDate.value    = review.date;
    form.achievements.value  = review.achievements;
    form.problems.value      = review.problems;
    form.learnings.value     = review.learnings;
    form.tomorrow.value      = review.tomorrow;
    if (review.mood) {
      const radio = form.querySelector(`input[name="mood"][value="${review.mood}"]`);
      if (radio) radio.checked = true;
    }
  }

  function resetForm() {
    form.reset();
    setTodayDate();
    editingId = null;
    formTitle.textContent   = '新建复盘';
    submitBtn.textContent   = '保存复盘';
    cancelBtn.style.display = 'none';
  }

  /* ---------- Toggle form collapse ---------- */
  toggleFormBtn.addEventListener('click', () => {
    const isCollapsed = form.classList.toggle('collapsed');
    toggleFormBtn.textContent = isCollapsed ? '▼' : '▲';
    toggleFormBtn.title       = isCollapsed ? '展开表单' : '收起表单';
  });

  /* ---------- Cancel edit ---------- */
  cancelBtn.addEventListener('click', () => {
    resetForm();
  });

  /* ---------- Submit ---------- */
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = getFormData();

    if (!data.date) {
      showToast('请选择日期', 'error');
      return;
    }
    if (!data.achievements) {
      showToast('请填写今日成就', 'error');
      return;
    }

    if (editingId) {
      const idx = reviews.findIndex(r => r.id === editingId);
      if (idx !== -1) {
        reviews[idx] = { ...reviews[idx], ...data, updatedAt: Date.now() };
        showToast('复盘已更新 ✓', 'success');
      }
    } else {
      reviews.push({ id: generateId(), ...data, createdAt: Date.now() });
      showToast('复盘已保存 ✓', 'success');
    }

    saveReviews();
    resetForm();
    renderList();
  });

  /* ---------- Render list ---------- */
  function renderList() {
    const query = searchInput.value.toLowerCase();
    const order = sortSelect.value;

    let filtered = reviews.filter(r => {
      if (!query) return true;
      return (
        r.date.includes(query) ||
        (r.achievements || '').toLowerCase().includes(query) ||
        (r.problems     || '').toLowerCase().includes(query) ||
        (r.learnings    || '').toLowerCase().includes(query) ||
        (r.tomorrow     || '').toLowerCase().includes(query)
      );
    });

    filtered.sort((a, b) =>
      order === 'asc'
        ? a.date.localeCompare(b.date)
        : b.date.localeCompare(a.date)
    );

    // Clear everything except emptyState
    Array.from(reviewList.children).forEach(el => {
      if (el !== emptyState) el.remove();
    });

    if (filtered.length === 0) {
      emptyState.style.display = '';
      return;
    }

    emptyState.style.display = 'none';

    filtered.forEach(review => {
      const item = createReviewItem(review);
      reviewList.appendChild(item);
    });
  }

  function createReviewItem(review) {
    const mood = review.mood ? MOOD_MAP[review.mood] : null;
    const preview = review.achievements || review.learnings || '（无内容）';

    const div = document.createElement('div');
    div.className = 'review-item';
    div.dataset.id = review.id;
    div.innerHTML = `
      <div class="review-item-header">
        <span class="review-item-date">${escapeHtml(formatDate(review.date))}</span>
        <div class="review-item-meta">
          ${mood ? `<span class="review-item-mood" title="${escapeHtml(mood.label)}">${mood.emoji}</span>` : ''}
          <div class="review-item-actions">
            <button class="btn btn-secondary edit-btn" data-id="${escapeHtml(review.id)}">编辑</button>
            <button class="btn btn-danger delete-btn" data-id="${escapeHtml(review.id)}">删除</button>
          </div>
        </div>
      </div>
      <p class="review-item-preview">${escapeHtml(preview)}</p>
      <div class="review-item-tags">
        ${review.achievements ? '<span class="tag">🌟 成就</span>'  : ''}
        ${review.problems     ? '<span class="tag">⚠️ 问题</span>'  : ''}
        ${review.learnings    ? '<span class="tag">💡 收获</span>'  : ''}
        ${review.tomorrow     ? '<span class="tag">🎯 计划</span>'  : ''}
      </div>
    `;

    // Open detail on card click (but not on button click)
    div.addEventListener('click', (e) => {
      if (e.target.closest('.edit-btn') || e.target.closest('.delete-btn')) return;
      openDetail(review.id);
    });

    div.querySelector('.edit-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      startEdit(review.id);
    });

    div.querySelector('.delete-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      openDeleteModal(review.id);
    });

    return div;
  }

  /* ---------- Edit ---------- */
  function startEdit(id) {
    const review = reviews.find(r => r.id === id);
    if (!review) return;

    editingId = id;
    populateForm(review);

    formTitle.textContent   = '编辑复盘';
    submitBtn.textContent   = '更新复盘';
    cancelBtn.style.display = '';

    // Expand form if collapsed
    form.classList.remove('collapsed');
    toggleFormBtn.textContent = '▲';
    toggleFormBtn.title       = '收起表单';

    formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /* ---------- Delete ---------- */
  function openDeleteModal(id) {
    deletingId = id;
    deleteModal.style.display = 'flex';
  }

  cancelDeleteBtn.addEventListener('click', () => {
    deleteModal.style.display = 'none';
    deletingId = null;
  });

  confirmDeleteBtn.addEventListener('click', () => {
    if (!deletingId) return;
    reviews = reviews.filter(r => r.id !== deletingId);
    saveReviews();
    renderList();
    deleteModal.style.display = 'none';
    deletingId = null;
    showToast('已删除', 'success');
  });

  deleteModal.addEventListener('click', (e) => {
    if (e.target === deleteModal) {
      deleteModal.style.display = 'none';
      deletingId = null;
    }
  });

  /* ---------- Detail ---------- */
  function openDetail(id) {
    const review = reviews.find(r => r.id === id);
    if (!review) return;

    const mood = review.mood ? MOOD_MAP[review.mood] : null;

    detailDate.textContent = formatDate(review.date);

    detailContent.innerHTML = `
      ${mood ? `
        <div class="detail-mood">${mood.emoji}</div>
        <div class="detail-mood-label">心情：${escapeHtml(mood.label)}</div>
      ` : ''}
      ${review.achievements ? `
        <div class="detail-section">
          <h4>🌟 今日成就</h4>
          <p>${escapeHtml(review.achievements)}</p>
        </div>
      ` : ''}
      ${review.problems ? `
        <div class="detail-section">
          <h4>⚠️ 遇到的问题</h4>
          <p>${escapeHtml(review.problems)}</p>
        </div>
      ` : ''}
      ${review.learnings ? `
        <div class="detail-section">
          <h4>💡 心得体会</h4>
          <p>${escapeHtml(review.learnings)}</p>
        </div>
      ` : ''}
      ${review.tomorrow ? `
        <div class="detail-section">
          <h4>🎯 明日计划</h4>
          <p>${escapeHtml(review.tomorrow)}</p>
        </div>
      ` : ''}
    `;

    editFromDetailBtn.dataset.id = id;
    detailModal.style.display = 'flex';
  }

  [closeDetailBtn, closeDetailBtn2].forEach(btn => {
    btn.addEventListener('click', () => {
      detailModal.style.display = 'none';
    });
  });

  detailModal.addEventListener('click', (e) => {
    if (e.target === detailModal) detailModal.style.display = 'none';
  });

  editFromDetailBtn.addEventListener('click', () => {
    const id = editFromDetailBtn.dataset.id;
    detailModal.style.display = 'none';
    startEdit(id);
  });

  /* ---------- Search & Sort ---------- */
  searchInput.addEventListener('input', renderList);
  sortSelect.addEventListener('change', renderList);

})();
