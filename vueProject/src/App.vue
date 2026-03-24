<template>
  <div>
    <router-view />
    
  </div>
</template>

<script>

export default {
  components: {  },
  data() {
    return {
    
    }
  },
  created() {
    window.addEventListener('beforeunload', this.clearLocalStorage);
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.clearLocalStorage);
  },
  methods: {
    clearLocalStorage() {
      localStorage.clear(); // Çå³ýlocalStorageµÄÄÚÈÝ
    }
  }
}
</script>

<style>

</style>
