<script setup>
defineProps({
  field: Object,
  form: Object,
  class: String,
});
</script>

<template>
  <select :class="class" :multiple="field.attrs.multiple" v-for="choice in field.choices">
    <option :value="choice[0]">{{ choice[1] }}</option>
  </select>
</template>
