import { useForm } from '@inertiajs/react';
import Button from '../components/Button';
import FormField from '../components/FormField';

export default function Form(form) {
  const { data, setData, post, processing, errors } = useForm(form.initial);
  const submit = (e) => {
    e.preventDefault();
    post(form.submitEndpoint || '', {
      forceFormData: true,
      preserveState: form?.preserveState === false ? false : true,
    });
  };

  return (
    <form onSubmit={submit}>
      <div className="grid gap-y-4">
        {form.fields.map((field) => (
          <FormField
            key={field.name}
            {...field}
            onChange={(e) => setData(field.name, e.target.value)}
            value={data?.[field.name]}
            errors={errors?.[field.name]}
          />
        ))}

        <Button
          type="submit"
          loading={processing}
          className="py-3 px-4 inline-flex justify-center items-center gap-2 rounded-md border border-transparent font-semibold bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all text-sm dark:focus:ring-offset-gray-800"
        >
          {form.submit_button_text}
        </Button>
      </div>
      {errors.__all__ && (
        <p className="text-xs text-red-600 mt-2" id="all-error">
          {errors.__all__.map((error) => error.message)}
        </p>
      )}
    </form>
  );
}
