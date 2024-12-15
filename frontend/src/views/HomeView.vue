<template>
  <div class="home">
    <aside class="home__sidebar">
      <div class="filters-container">
        <CategoryFilter class="filter-section" />
        <ReadStatusFilter class="filter-section" />
      </div>
    </aside>
    <main class="home__main">
      <PaperGrid />
    </main>
  </div>
</template>

<script setup>
import CategoryFilter from '../components/CategoryFilter.vue';
import ReadStatusFilter from '../components/ReadStatusFilter.vue';
import PaperGrid from '../components/PaperGrid.vue';
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.home {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: $spacing-unit * 3;
  height: calc(100vh - 64px);

  &__sidebar {
    position: sticky;
    top: 64px;
    height: calc(100vh - 64px);
    overflow: hidden;
    padding: $spacing-unit * 3;
  }

  &__main {
    padding: $spacing-unit * 3;
    overflow-y: auto;
  }

  @media (max-width: $breakpoint-lg) {
    grid-template-columns: 1fr;
    height: auto;
    
    &__sidebar {
      position: relative;
      height: auto;
      top: 0;
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
</style> 