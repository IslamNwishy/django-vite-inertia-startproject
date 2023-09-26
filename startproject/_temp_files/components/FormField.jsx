import Select from './FormInputs/Select';
import Switch from './FormInputs/Switch';

function Input(props) {
  const finalProps = {
    ...props.attrs,
    value: props.value,
    onChange: props.onChange,
    className: props?.className || '',
  };
  switch (props.attrs.type) {
    case 'select':
      return <Select {...finalProps} choices={props.choices} />;
    case 'checkbox':
      return <Switch {...finalProps} />;
    case 'textarea':
      return <textarea {...finalProps} />;
    default:
      return <input {...finalProps} />;
  }
}
export default function FormField(props) {
  console.log(props);
  return (
    <div>
      <label htmlFor={props.id} className="block text-sm mb-2 dark:text-white">
        {props.label}
      </label>
      <div className="relative">
        {
          <Input
            {...props}
            className="py-3 px-4 block w-full border-gray-200 rounded-md text-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400"
          />
        }
      </div>
      {props.errors && (
        <p className="text-xs text-red-600 mt-2" id={`${props.name}-error`}>
          {props.errors.map((error) => error.message)}
        </p>
      )}
    </div>
  );
}
