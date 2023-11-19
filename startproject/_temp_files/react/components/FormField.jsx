import { InformationCircleIcon } from '@heroicons/react/24/solid';
import { Tooltip } from 'flowbite-react';
import { nanoid } from 'nanoid';
import FileField from './FormInputs/FileField';
import PaginatedSelect from './FormInputs/PaginatedSelect';
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
      return props.limit ? (
        <PaginatedSelect
          {...finalProps}
          choices={props.choices}
          offset={props.offset}
          limit={props.limit}
          name={props.name}
        />
      ) : (
        <Select {...finalProps} choices={props.choices} />
      );
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

  const newId = nanoid();

  return (
    <div className={props.wrapperClass || 'mt-2'}>
      <div className="flex items-center justify-between pb-2 pt-4">
        <label htmlFor={newId} className="block text-sm font-medium leading-6 text-gray-900">
          {props.label}
        </label>
        {props.help_text ? (
          <>
            <Tooltip
              content={
                <div dangerouslySetInnerHTML={{ __html: props.help_text }} className="mt-1 text-sm text-white"></div>
              }
            >
              <InformationCircleIcon
                data-tooltip-target={newId}
                data-tooltip-trigger="hover"
                type="button"
                className="h-6 w-6"
              />
            </Tooltip>
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
