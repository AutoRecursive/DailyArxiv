<template>
  <div class="home">
    <CategoryFilter class="home__filter" />
    <PaperGrid class="home__grid" />
  </div>
</template>

<script setup>
import CategoryFilter from '../components/CategoryFilter.vue';
import PaperGrid from '../components/PaperGrid.vue';
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.home {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: $spacing-unit * 3;
  padding: $spacing-unit * 3;

  @media (max-width: $breakpoint-lg) {
    grid-template-columns: 1fr;
  }

  &__filter {
    background: white;
    border-radius: $card-border-radius;
    height: fit-content;
    position: sticky;
    top: 80px;
  }
}
</style> 