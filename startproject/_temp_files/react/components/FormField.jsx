import { InformationCircleIcon } from '@heroicons/react/24/solid';
import FileField from './FormInputs/FileField';
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
    case 'file':
      return (
        <FileField
          {...finalProps}
          name={props.name}
          onClearChanged={(extras, options) =>
            props.manualSubmit({ [`${props.name}-clear`]: true, ...extras }, options)
          }
        />
      );
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
  if (props.attrs.type == 'hidden') return <Input {...props} />;
  if (props.customComponent) return props.customComponent(props);

  const defaultClasses =
    'block w-full rounded-md border-0 py-1.5 mb-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6 disabled:opacity-50 disabled:bg-gray-200 placeholder:text-gray-500';
  return (
    <div className={props.wrapperClass || 'mt-2'}>
      <div className="flex items-center justify-between pb-2 pt-4">
        <label htmlFor={props.id} className="block text-sm font-medium leading-6 text-gray-900">
          {props.label}
        </label>
        {props.help_text ? (
          <>
            <InformationCircleIcon data-tooltip-target={props.id} className="h-6 w-6" />
            {/* <button
              data-tooltip-target="tooltip-default"
              type="button"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Default tooltip
            </button> */}
            <div
              id={props.id}
              role="tooltip"
              class="absolute z-10 invisible inline-block px-3 py-2 text-sm font-medium text-white transition-opacity duration-300 bg-gray-900 rounded-lg shadow-sm opacity-0 tooltip dark:bg-gray-700"
            >
              <div dangerouslySetInnerHTML={{ __html: props.help_text }} className="mt-1 text-sm text-white"></div>
              <div class="tooltip-arrow" data-popper-arrow></div>
            </div>
          </>
        ) : null}

        {props.labelSuffix}
      </div>

      <div className="flex flex-start">{<Input {...props} className={props.className || defaultClasses} />}</div>

      {props.errors && (
        <p className="text-xs text-red-600 mt-2" id={`${props.name}-error`}>
          {props.errors.map((error) => error.message || error)}
        </p>
      )}
    </div>
  );
}
