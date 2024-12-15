<template>
  <div class="paper-grid">
    <div v-if="isLoading" class="loading">
      Loading papers...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else-if="papers.length === 0" class="no-papers">
      No papers found. Try refreshing or changing filters.
    </div>
    <template v-else>
      <PaperCard
        v-for="paper in papers"
        :key="paper.id"
        :paper="paper"
      />
    </template>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { usePapersStore } from '../stores/papers';
import PaperCard from './PaperCard.vue';

const store = usePapersStore();

onMounted(async () => {
  await store.fetchPapers();
});

const papers = computed(() => store.filteredPapers);
const isLoading = computed(() => store.isLoading);
const error = computed(() => store.error);
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.paper-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: $spacing-unit * 2;
  padding: $spacing-unit * 2;
}

.loading, .error, .no-papers {
  grid-column: 1 / -1;
  text-align: center;
  padding: $spacing-unit * 4;
  @include themed() {
    background: t('card-background');
  }
  border-radius: $card-border-radius;
}

.error {
  @include themed() {
    color: t('primary-color');
  }
}
</style> 