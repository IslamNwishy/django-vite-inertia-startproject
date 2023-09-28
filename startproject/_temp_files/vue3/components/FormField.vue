<script setup>
import Select from './FormInputs/Select.vue';
import Switch from './FormInputs/Switch.vue';

defineProps({
  field: Object,
  errors: Object,
  form: Object,
});
const input_field_classes =
  'py-3 px-4 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400';
</script>

<template>
  <div>
    <label :for="field.name" class="block text-sm mb-2 dark:text-white">
      {{ field.label }}
    </label>
    <div class="relative">
      <Switch :field="field" :form="form" v-if="field.attrs.type == 'checkbox' && !field.attrs.plain" />
      <Select
        :field="field"
        :form="form"
        v-else-if="field.attrs.type == 'select'"
        :class="input_field_classes"
      ></Select>
      <input v-else v-bind="field.attrs" v-model="form[field.name]" :class="input_field_classes" />

      <div v-if="errors">
        <p class="text-xs text-red-600 mt-2" v-for="error in errors">
          {{ error.message }}
        </p>
      </div>
    </div>
  </div>
</template>
