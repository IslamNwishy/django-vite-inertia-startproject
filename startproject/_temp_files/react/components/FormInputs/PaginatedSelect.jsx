import { Combobox } from '@headlessui/react';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid';
import { router } from '@inertiajs/react';
import { useState } from 'react';
import setupProps from '../../utils/setupProps';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function PaginatedSelect(props) {
  const [query, setQuery] = useState(props.query);
  const [choices, setChoices] = useState(props.choices);
  const [filtered, setFiltered] = useState(props.choices);
  const [offset, setOffset] = useState(props.offset);
  const [choicesStatus, setChoicesStatus] = useState('idle');
  const statusText = {
    idle: 'Scroll for more...',
    loading: 'Loading more...',
    finished: 'No more options',
  };
  const retrieveChoices = (offset, searchQuery) => {
    router.get(
      '',
      {
        field: props.name,
        offset: offset,
        query: searchQuery,
      },
      {
        preserveState: true,
        preserveScroll: true,
        only: ['paginate'],
        onStart: () => {
          setChoicesStatus('loading');
        },
        onSuccess: (page) => {
          const isPagination = query === searchQuery;
          const { newOffset, newChoices } = page.props?.paginate;
          if (newChoices && newChoices?.length > 0) {
            if (!isPagination) {
              setChoices(newChoices);
            } else {
              setChoices((choices) => [...choices, ...newChoices]);
            }
            setOffset(newOffset);
            setChoicesStatus('idle');
          } else {
            if (!isPagination) setChoices(newChoices);
            setChoicesStatus('finished');
          }
          page = setupProps(page);
        },
      }
    );
  };

  const handleScroll = (event) => {
    const { scrollTop, scrollHeight, clientHeight } = event.target;
    const threshold = 50; // Threshold in pixels for determining when to trigger the function

    if (Math.round(scrollTop) + Math.round(clientHeight) >= Math.round(scrollHeight) - threshold) {
      // Execute the function when the user reaches the end of the options

      if (choicesStatus === 'idle') {
        retrieveChoices(offset, query);
      }
    }
  };
  const handleQueryChange = (event) => {
    const newQuery = event.target.value;
    if (query === newQuery) return;
    setQuery(newQuery);
    setOffset(0);
    retrieveChoices(0, newQuery);

    // const newFiltered = choices.filter((item) => item[1].toLowerCase().includes(newQuery.toLowerCase()));
    // setFiltered(newFiltered);
  };

  return (
    <>
      <div className="text-start w-full">
        <Combobox as="div" value={props.value} onChange={(value) => props.onChange({ target: { value: value } })}>
          <Combobox.Label className="block text-sm font-medium leading-6 text-gray-900">
            {/* Label Text */}
          </Combobox.Label>

          <div className="relative mt-2">
            <Combobox.Input
              placeholder={props?.placeholder}
              className="w-full rounded-md border-0 bg-white py-1.5 pl-3 pr-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-yellow-600 sm:text-sm sm:leading-6"
              onChange={handleQueryChange}
              displayValue={(option) => {
                return choices.find((item) => item[0] == option)?.[1];
              }}
            />

            <Combobox.Button className="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
              <ChevronUpDownIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
            </Combobox.Button>

            {choices && (
              <Combobox.Options
                className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                onScroll={handleScroll}
              >
                {choices.map((option) => (
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
                <Combobox.Option key="status" disabled>
                  <div className="flex justify-center items-center py-2">
                    <div className="text-gray-400">{statusText[choicesStatus]}</div>
                  </div>
                </Combobox.Option>
              </Combobox.Options>
            )}
          </div>
        </Combobox>
      </div>
    </>
  );
}
