<template>
  <div class="paper-card" @click="navigateToPaper">
    <div class="paper-card__image" @contextmenu.prevent="navigateToPaper">
      <img :src="getImageForCategory(paper.categories)" :alt="paper.title" @contextmenu.prevent>
      <button 
        class="read-status-btn"
        :class="{ 'is-read': isRead }"
        @click.stop="toggleReadStatus"
        :title="isRead ? 'Mark as unread' : 'Mark as read'"
      >
        <span class="icon">{{ isRead ? '✓' : '○' }}</span>
      </button>
    </div>
    <div class="paper-card__content">
      <div class="paper-card__categories">
        <span v-for="category in mainCategories" 
              :key="category" 
              class="category-tag">
          {{ category }}
        </span>
      </div>
      <h3 class="paper-card__title">{{ paper.title }}</h3>
      <p class="paper-card__abstract">{{ truncatedAbstract }}</p>
      <div class="paper-card__footer">
        <span class="paper-card__date">{{ formatDate(paper.published_date) }}</span>
        <div class="paper-card__links">
          <a :href="getArxivUrl(paper.id)" 
             target="_blank" 
             class="paper-card__link"
             @click.stop>
            arXiv
          </a>
          <a :href="paper.pdf_url" 
             target="_blank" 
             class="paper-card__link"
             @click.stop>
            PDF
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useReadStatusStore } from '../stores/readStatus';

const props = defineProps({
  paper: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const readStatusStore = useReadStatusStore();
const isRead = computed(() => readStatusStore.isRead(props.paper.id));

const mainCategories = computed(() => {
  return props.paper.categories.split(', ').slice(0, 2);
});

const truncatedAbstract = computed(() => {
  return props.paper.abstract.length > 150
    ? props.paper.abstract.slice(0, 150) + '...'
    : props.paper.abstract;
});

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString();
}

const CATEGORY_IMAGES = {
  'cs.CV': '/images/categories/computer-vision.jpg',
  'cs.LG': '/images/categories/machine-learning.jpg',
  'cs.AI': '/images/categories/artificial-intelligence.jpg',
  'cs.CL': '/images/categories/computational-linguistics.jpg',
  'cs.RO': '/images/categories/robotics.jpg'
};

const DEFAULT_IMAGE = '/images/categories/default.jpg';

function getImageForCategory(categories) {
  const mainCategory = categories.split(',')[0].trim();
  return CATEGORY_IMAGES[mainCategory] || DEFAULT_IMAGE;
}

function getArxivUrl(paperId) {
  return `https://arxiv.org/abs/${paperId}`;
}

function toggleReadStatus() {
  readStatusStore.toggleRead(props.paper.id);
}

function navigateToPaper() {
  readStatusStore.markAsRead(props.paper.id);
  window.open(getArxivUrl(props.paper.id), '_blank');
}
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.paper-card {
  @include themed() {
    background: t('card-background');
  }
  border-radius: $card-border-radius;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 420px;

  &:hover {
    transform: translateY(-4px);
    @include themed() {
      box-shadow: 0 8px 16px t('shadow-color');
    }
  }

  &__image {
    width: 100%;
    height: 160px;
    overflow: hidden;
    position: relative;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    padding: $spacing-unit * 1.5;
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  &__categories {
    margin-bottom: $spacing-unit;
    display: flex;
    flex-wrap: wrap;
    gap: $spacing-unit * 0.5;
  }

  &__title {
    font-size: 1rem;
    margin-bottom: $spacing-unit;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    @include themed() {
      color: t('text-primary');
    }
  }

  &__abstract {
    font-size: 0.9rem;
    margin-bottom: $spacing-unit;
    flex: 1;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    @include themed() {
      color: t('text-secondary');
    }
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    margin-top: auto;
    @include themed() {
      color: t('text-secondary');
    }
  }

  &__links {
    display: flex;
    gap: $spacing-unit;
  }

  &__link {
    text-decoration: none;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background-color 0.2s;
    font-size: 0.85rem;
    @include themed() {
      color: t('primary-color');
      
      &:hover {
        background-color: rgba(t('primary-color'), 0.1);
      }
    }
  }
}

.category-tag {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  transition: all 0.2s;
  @include themed() {
    background: t('category-bg');
    color: t('category-text');
    border: 1px solid t('category-text');
    
    &:hover {
      background: t('category-text');
      color: t('card-background');
    }
  }
}

.read-status-btn {
  position: absolute;
  top: $spacing-unit;
  right: $spacing-unit;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  opacity: 0;
  z-index: 1;
  
  @include themed() {
    background: t('card-background');
    color: t('text-secondary');
    box-shadow: 0 2px 4px t('shadow-color');
    
    &:hover {
      background: t('primary-color');
      color: t('card-background');
      transform: scale(1.1);
    }
    
    &.is-read {
      opacity: 1;
      background: t('primary-color');
      color: t('card-background');
    }
  }
  
  .icon {
    font-size: 1rem;
    line-height: 1;
  }
}

.paper-card:hover .read-status-btn {
  opacity: 1;
}

.paper-card.is-read {
  @include themed() {
    opacity: 0.75;
    
    &:hover {
      opacity: 0.9;
    }
  }
}
</style> 