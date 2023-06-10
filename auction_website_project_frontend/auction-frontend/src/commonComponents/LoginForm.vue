<template>
  <form>
    <h3 class="mb-4">Login</h3>
    <v-text-field
      v-model="formData.login"
      label="Login"
      variant="outlined"
    ></v-text-field>
    <v-text-field
      v-model="formData.password"
      label="Password"
      type="password"
      variant="outlined"
    ></v-text-field>
    <Button button-text="login" @click="handleSubmit" />
  </form>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import Button from "./Button.vue";

const formData = reactive({
  login: "",
  password: "",
});

function handleSubmit(e: MouseEvent): void {
  e.preventDefault();
}
</script>

<style scoped lang="scss">
form {
  margin: 0 1em;
  min-width: 260px;
  max-width: 360px;
  width: 90%;
  padding: 2em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 4px 8px 20px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}
</style>
