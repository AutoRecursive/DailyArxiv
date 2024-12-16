<template>
  <div class="home">
    <button 
      class="filters-toggle"
      :class="{ 'filters-visible': isFiltersVisible }"
      @click="toggleFilters"
      v-show="isMobile"
    >
      <span class="icon">{{ isFiltersVisible ? '×' : '☰' }}</span>
      <span class="text">{{ isFiltersVisible ? 'Close' : 'Filters' }}</span>
    </button>

    <aside 
      class="home__sidebar"
      :class="{ 'is-visible': !isMobile || isFiltersVisible }"
    >
      <div class="filters-container">
        <CategoryFilter class="filter-section" />
        <ReadStatusFilter class="filter-section" />
      </div>
    </aside>

    <main class="home__main">
      <PaperGrid />
    </main>

    <div 
      class="overlay" 
      v-if="isMobile && isFiltersVisible"
      @click="toggleFilters"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import CategoryFilter from '../components/CategoryFilter.vue';
import ReadStatusFilter from '../components/ReadStatusFilter.vue';
import PaperGrid from '../components/PaperGrid.vue';

const isFiltersVisible = ref(false);
const isMobile = ref(false);

function toggleFilters() {
  isFiltersVisible.value = !isFiltersVisible.value;
  if (isFiltersVisible.value) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

function checkMobile() {
  isMobile.value = window.innerWidth <= 1024;
  if (!isMobile.value) {
    isFiltersVisible.value = false;
    document.body.style.overflow = '';
  }
}

onMounted(() => {
  checkMobile();
  window.addEventListener('resize', checkMobile);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile);
});
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.home {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: $spacing-unit * 3;
  height: calc(100vh - 64px);
  position: relative;

  &__sidebar {
    position: sticky;
    top: 64px;
    height: calc(100vh - 64px);
    overflow: hidden;
    padding: $spacing-unit * 3;
    z-index: 100;
    transition: transform 0.3s ease;

    @include themed() {
      background: t('background-color');
    }
  }

  &__main {
    padding: $spacing-unit * 3;
    overflow-y: auto;
  }

  @media (max-width: $breakpoint-lg) {
    grid-template-columns: 1fr;

    &__sidebar {
      position: fixed;
      top: 0;
      left: 0;
      width: 300px;
      height: 100vh;
      transform: translateX(-100%);
      padding-top: 80px;

      &.is-visible {
        transform: translateX(0);
      }
    }
  }
}

.filters-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: $spacing-unit * 2;
}

.filter-section {
  @include themed() {
    background: t('card-background');
  }
  border-radius: $card-border-radius;
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.filters-toggle {
  position: fixed;
  bottom: $spacing-unit * 3;
  right: $spacing-unit * 3;
  z-index: 1000;
  padding: $spacing-unit * 1.5;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: $spacing-unit;
  transition: all 0.3s ease;
  
  @include themed() {
    background: t('primary-color');
    color: t('card-background');
    box-shadow: 0 2px 8px t('shadow-color');
    
    &:hover {
      background: t('secondary-color');
      transform: translateY(-2px);
    }

    &.filters-visible {
      background: t('text-secondary');
    }
  }

  .icon {
    font-size: 1.2rem;
  }

  .text {
    font-size: 0.9rem;
    font-weight: 500;
  }
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 90;
  @include themed() {
    background: rgba(t('background-color'), 0.8);
  }
  backdrop-filter: blur(4px);
}
</style> 