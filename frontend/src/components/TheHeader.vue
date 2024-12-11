<template>
  <header class="header">
    <div class="container header__content">
      <h1 class="header__title">ArXiv Papers</h1>
      <div class="header__actions">
        <ThemeSwitch />
        <button class="refresh-btn" @click="refreshPapers" :disabled="isLoading">
          <span v-if="isLoading">Updating...</span>
          <span v-else>Refresh Papers</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { usePapersStore } from '../stores/papers';
import ThemeSwitch from './ThemeSwitch.vue';

const store = usePapersStore();
const isLoading = ref(false);

async function refreshPapers() {
  isLoading.value = true;
  try {
    await store.updatePapers();
  } finally {
    isLoading.value = false;
  }
}
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.header {
  @include themed() {
    background: t('card-background');
    box-shadow: 0 2px 4px t('shadow-color');
  }
  position: sticky;
  top: 0;
  z-index: 100;
  transition: background-color 0.3s, box-shadow 0.3s;

  &__content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
  }

  &__title {
    font-size: 1.5rem;
    @include themed() {
      color: t('primary-color');
    }
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: $spacing-unit * 2;
  }
}

.refresh-btn {
  @include themed() {
    background: t('secondary-color');
    color: t('card-background');
    
    &:hover:not(:disabled) {
      background: t('accent-color');
    }
  }
  border: none;
  padding: $spacing-unit $spacing-unit * 2;
  border-radius: $card-border-radius;
  cursor: pointer;
  transition: all 0.2s;

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}
</style> 