<template>
  <div class="category-filter">
    <h3 class="filter-header">Categories</h3>
    <div class="filter-content">
      <div class="category-list">
        <button
          v-for="category in categories"
          :key="category.category"
          :class="['category-btn', { active: isSelected(category.category) }]"
          @click="toggleCategory(category.category)"
        >
          {{ category.category }}
          <span class="count">({{ category.count }})</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { usePapersStore } from '../stores/papers';

const store = usePapersStore();

onMounted(async () => {
  await store.fetchCategories();
});

const categories = computed(() => store.categories);
const selectedCategory = computed(() => store.selectedCategory);

function isSelected(category) {
  return selectedCategory.value === category;
}

function toggleCategory(category) {
  store.setSelectedCategory(category === selectedCategory.value ? null : category);
}
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.category-filter {
  display: flex;
  flex-direction: column;
  height: 100%;
  
  .filter-header {
    padding: $spacing-unit * 2;
    margin: 0;
    @include themed() {
      color: t('text-primary');
    }
  }
  
  .filter-content {
    flex: 1;
    overflow-y: auto;
    padding: 0 $spacing-unit * 2 $spacing-unit * 2;
    
    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-track {
      @include themed() {
        background: t('background-color');
      }
    }

    &::-webkit-scrollbar-thumb {
      @include themed() {
        background: t('border-color');
        &:hover {
          background: t('text-secondary');
        }
      }
      border-radius: 2px;
    }
  }
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-unit;
}

.category-btn {
  padding: $spacing-unit $spacing-unit * 2;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  
  @include themed() {
    background: t('category-bg');
    color: t('category-text');
    border: 1px solid t('category-text');
    
    &:hover {
      background: rgba(t('category-text'), 0.2);
    }
    
    &.active {
      background: t('primary-color');
      color: t('card-background');
      border-color: t('primary-color');
    }
  }

  .count {
    opacity: 0.7;
    margin-left: 4px;
  }
}
</style> 