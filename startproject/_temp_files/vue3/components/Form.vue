<script setup>
import { useForm } from '@inertiajs/vue3';
import Button from './Button.vue';
import FormField from './FormField.vue';

const props = defineProps({ form: Object });
const newForm = useForm(props.form.initial);
const submit = () => {
  newForm
    .transform((data) => {
      const formData = new FormData();
      for (const key of Object.keys(data)) {
        const value = data[key];
        if (Array.isArray(value)) for (const val of value) formData.append(key, val);
        else formData.append(key, data[key]);
      }
      return formData;
    })
    .post('', { forceFormData: true, preserveScroll: true });
};
</script>

<template>
  <form @submit.prevent="submit">
    <div class="grid gap-y-4">
      <div v-for="field in form.fields">
        <FormField :field="field" :errors="newForm.errors?.[field.name]" :form="newForm" />
      </div>
      <Button
        type="submit"
        :loading="newForm.processing"
        class="py-3 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800"
      >
        {{ form.submit_button_text }}
      </Button>
    </div>
    <div v-if="newForm.errors.__all__">
      <p class="text-xs text-red-600 mt-2" v-for="error in newForm.errors.__all__">
        {{ error.message }}
      </p>
    </div>
  </form>
</template>
