import { Combobox } from '@headlessui/react';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid';
import { useState } from 'react';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function Select(props) {
  const [query, setQuery] = useState('');

  if (props.searchable) {
    const filtered =
      query === ''
        ? props.choices
        : props.choices.filter((choice) => {
            return choice[1].toLowerCase().includes(query.toLowerCase());
          });

    return (
      <>
        <div className="text-start w-full">
          <Combobox as="div" value={props.value} onChange={(value) => props.onChange({ target: { value: value } })}>
            <Combobox.Label className="block text-sm font-medium leading-6 text-gray-900">
              {/* Label Text */}
            </Combobox.Label>
            <div className="relative mt-2">
              <Combobox.Input
                className="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6"
                onChange={(event) => setQuery(event.target.value)}
                displayValue={(option) => {
                  return props.choices.find((item) => item[0] == option)?.[1];
                }}
              />
              <Combobox.Button className="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
                <ChevronUpDownIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </Combobox.Button>

              {filtered.length > 0 && (
                <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                  {filtered.map((option) => (
                    <Combobox.Option
                      key={option[0]}
                      value={option[0]}
                      className={({ active }) =>
                        classNames(
                          'relative cursor-pointer select-none py-2 pl-3 pr-9',
                          active ? 'bg-yellow-600 text-white' : 'text-gray-900'
                        )
                      }
                    >
                      {({ active, selected }) => (
                        <>
                          <span className={classNames('block truncate', selected && 'font-semibold')}>{option[1]}</span>

                          {selected && (
                            <span
                              className={classNames(
                                'absolute inset-y-0 right-0 flex items-center pr-4',
                                active ? 'text-white' : 'text-yellow-600'
                              )}
                            >
                              <CheckIcon className="h-5 w-5" aria-hidden="true" />
                            </span>
                          )}
                        </>
                      )}
                    </Combobox.Option>
                  ))}
                </Combobox.Options>
              )}
            </div>
          </Combobox>
        </div>
      </>
    );
  }

  return (
    <select
      {...props}
      {...(props.multiple
        ? {
            onChange: (e) =>
              props.onChange({ target: { value: Array.from(e.target.selectedOptions).map((option) => option.value) } }),
          }
        : {})}
    >
      {props.choices.map((choice, index) => (
        <option value={choice[0]} key={index}>
          {choice[1]}
        </option>
      ))}
    </select>
  );
}
