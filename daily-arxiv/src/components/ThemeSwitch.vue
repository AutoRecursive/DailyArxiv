<template>
  <div class="theme-switch">
    <button 
      v-for="theme in themes" 
      :key="theme.name"
      :class="['theme-btn', { active: currentTheme === theme.name }]"
      @click="setTheme(theme.name)"
    >
      {{ theme.icon }} {{ theme.label }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useThemeStore } from '../stores/theme';

const themeStore = useThemeStore();
const currentTheme = computed(() => themeStore.currentTheme);

const themes = [
  { name: 'cyberpunk', label: '赛博朋克', icon: '🌟' },
  { name: 'light', label: '浅色', icon: '☀️' },
  { name: 'dark', label: '深色', icon: '🌙' }
];

function setTheme(theme) {
  themeStore.setTheme(theme);
}
</script>

<style lang="scss" scoped>
@use '../assets/styles/index' as *;

.theme-switch {
  display: flex;
  gap: $spacing-unit;
}

.theme-btn {
  background: none;
  border: none;
  padding: $spacing-unit $spacing-unit * 2;
  border-radius: $card-border-radius;
  cursor: pointer;
  transition: all 0.2s;
  
  @include themed() {
    color: t('text-primary');
    border: 1px solid t('border-color');
    
    &:hover {
      background-color: t('border-color');
    }
    
    &.active {
      background-color: t('primary-color');
      color: white;
      border-color: t('primary-color');
    }
  }
}
</style> 