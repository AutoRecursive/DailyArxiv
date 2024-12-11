<template>
  <div class="paper-card" @click="navigateToPaper">
    <div class="paper-card__image">
      <img :src="getImageForCategory(paper.categories)" :alt="paper.title">
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

const props = defineProps({
  paper: {
    type: Object,
    required: true
  }
});

const router = useRouter();

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

function navigateToPaper() {
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

  &:hover {
    transform: translateY(-4px);
    @include themed() {
      box-shadow: 0 8px 16px t('shadow-color');
    }
  }

  &__image {
    width: 100%;
    height: 200px;
    overflow: hidden;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  &__content {
    padding: $spacing-unit * 2;
  }

  &__categories {
    margin-bottom: $spacing-unit;
    display: flex;
    gap: $spacing-unit;
  }

  &__title {
    font-size: 1.1rem;
    margin-bottom: $spacing-unit;
    line-height: 1.4;
    @include themed() {
      color: t('text-primary');
    }
  }

  &__abstract {
    font-size: 0.9rem;
    margin-bottom: $spacing-unit * 2;
    @include themed() {
      color: t('text-secondary');
    }
  }

  &__footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.9rem;
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
    @include themed() {
      color: t('primary-color');
      
      &:hover {
        background-color: rgba(t('primary-color'), 0.1);
      }
    }
  }
}

.category-tag {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
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
</style> 