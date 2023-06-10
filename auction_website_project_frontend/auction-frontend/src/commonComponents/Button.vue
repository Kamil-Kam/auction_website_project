<template>
  <v-btn
    :disabled="disabled"
    :class="buttonClass"
    @click="emit('click', $event)"
    >{{ buttonText }}</v-btn
  >
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (event: "click", val: MouseEvent): void;
}>();

defineProps({
  buttonText: { type: String, required: true },
  disabled: { type: Boolean, required: false, default: false },
  buttonClass: { type: String, required: false, default: "" },
});
</script>
