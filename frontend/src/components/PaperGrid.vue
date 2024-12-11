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
  grid-template-columns: repeat(auto-fill, minmax($card-width, 1fr));
  gap: $card-gap;
  padding: $spacing-unit * 3;
}

.loading, .error, .no-papers {
  grid-column: 1 / -1;
  text-align: center;
  padding: $spacing-unit * 4;
  background: white;
  border-radius: $card-border-radius;
}

.error {
  color: red;
}
</style> 