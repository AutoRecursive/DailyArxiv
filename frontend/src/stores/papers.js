import { defineStore } from 'pinia';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const usePapersStore = defineStore('papers', {
  state: () => ({
    papers: [],
    categories: [],
    selectedCategory: null,
    isLoading: false,
    error: null
  }),

  getters: {
    filteredPapers: (state) => {
      if (!state.selectedCategory) return state.papers;
      return state.papers.filter(paper => 
        paper.categories.includes(state.selectedCategory)
      );
    }
  },

  actions: {
    async fetchPapers() {
      this.isLoading = true;
      try {
        const response = await axios.get(`${API_BASE_URL}/papers/recent`, {
          params: {
            days: 7,
            limit: 100
          }
        });
        this.papers = response.data;
        this.error = null;
      } catch (error) {
        console.error('Error fetching papers:', error);
        this.error = 'Failed to fetch papers';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchCategories() {
      try {
        const response = await axios.get(`${API_BASE_URL}/papers/categories`);
        this.categories = response.data;
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },

    async updatePapers() {
      try {
        await axios.post(`${API_BASE_URL}/papers/update`);
        // 更新后重新获取数据
        await this.fetchPapers();
        await this.fetchCategories();
      } catch (error) {
        console.error('Error updating papers:', error);
      }
    },

    setSelectedCategory(category) {
      this.selectedCategory = category;
    }
  }
}); 