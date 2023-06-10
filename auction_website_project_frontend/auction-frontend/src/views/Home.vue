<template>
  <main>
    <LoginForm />
  </main>
</template>

<script lang="ts" setup>
import LoginForm from "@/components/LoginForm.vue";
</script>

<style scoped lang="scss">
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
</style>
