import { router, useForm } from '@inertiajs/react';
import Button from '../components/Button';
import FormField from '../components/FormField';

export default function Form({
  form,
  className,
  buttonClasses,
  buttonWrapperClasses,
  buttonExtras,
  fieldModifiers,
  fieldsWrapperClasses,
  fieldWrapperClasses,
  preserveState,
  preserveScroll,
  submitEndpoint,
  preFieldschildren,
  postFieldsChildren,
}) {
  const { data, transform, setData, post, processing, errors } = useForm(form.initial);
  const submit = (e) => {
    e.preventDefault();
    post(submitEndpoint || '', {
      forceFormData: true,
      preserveState: preserveState === false ? false : true,
      preserveScroll: preserveScroll === false ? false : true,
    });
  };

  const makeFormData = (data) => {
    const formData = new FormData();
    for (const key of Object.keys(data)) {
      const value = data[key];
      if (Array.isArray(value)) for (const val of value) formData.append(key, val);
      else formData.append(key, data[key]);
    }

    return formData;
  };
  transform(makeFormData);

  const manualSubmit = (newData, options) => {
    const manualData = { ...data, ...newData };
    router.post(submitEndpoint || '', makeFormData(manualData), {
      forceFormData: true,
      preserveState: preserveState === false ? false : true,
      preserveScroll: preserveScroll === false ? false : true,
      ...options,
    });
  };
  return (
    <form onSubmit={submit} className={className}>
      {preFieldschildren}
      <div className={fieldsWrapperClasses}>
        {form.fields.map((field) => (
          <FormField
            key={field.name}
            {...field}
            onChange={(e) => setData(field.name, e.target.value)}
            manualSubmit={manualSubmit}
            value={data?.[field.name]}
            errors={errors?.[field.name]}
            {...(fieldModifiers?.[field.name] || {
              wrapperClass: fieldWrapperClasses,
            })}
          />
        ))}
      </div>
      {postFieldsChildren}
      <div className={buttonWrapperClasses}>
        <Button type="submit mt-2" loading={processing} className={buttonClasses}>
          {form.submit_button_text}
        </Button>
        {buttonExtras}
      </div>
      {errors.__all__ && (
        <p className="text-xs text-red-600 mt-2" id="all-error">
          {errors.__all__.map((error) => error.message)}
        </p>
      )}
    </form>
  );
}
