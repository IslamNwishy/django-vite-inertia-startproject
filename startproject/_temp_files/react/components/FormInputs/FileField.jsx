import { PhotoIcon } from '@heroicons/react/24/solid';
export default function FileField(props) {
  return (
    <>
      {!props.value ? (
        <div className="col-span-full">
          <div className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-2 py-2">
            <div className="text-center">
              <PhotoIcon className="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
              <div className="mt-4 flex text-sm leading-6 text-gray-600">
                <label
                  htmlFor={props.name}
                  className="relative cursor-pointer rounded-md bg-white font-semibold text-amber-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-amber-600 focus-within:ring-offset-2 hover:text-amber-500"
                >
                  <span>Upload a file</span>
                  <input
                    id={props.name}
                    name={props.name}
                    type={props.type}
                    value=""
                    className="sr-only"
                    onChange={(e) => props.onChange({ target: { value: e.target.files[0] } })}
                  />
                </label>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs leading-5 text-gray-600">PNG, JPG, GIF up to 10MB</p>
            </div>
          </div>
        </div>
      ) : (
        <div className="col-span-full">
          {props.value && (
            <div className="mb-5">
              <img src={typeof props.value == 'string' ? props.value : URL.createObjectURL(props.value)} />
              <button
                type="button"
                onClick={() => props.onClearChanged({ stay: true }, { preserveState: false })}
                className="text-black underline cursor-pointer"
              >
                Remove Image
              </button>
            </div>
          )}
        </div>
      )}
    </>
  );

  {
    /* <input
    {...props}
    value=""
    onChange={(e) => props.onChange({ target: { value: e.target.files[0] } })}
    className="file-input file-input-bordered file-input-md file-input-primary w-full max-w-xs"
  /> */
  }
  // <div className="mb-2 md:mb-0 md:py-2">
  //   <div className="my-4 flex flex-row items-center gap-2">
  //     <div className="p-2 px-2 bg-gray-50 border-2 border-gray-200 rounded-full">
  //       <svg
  //         className="text-sm"
  //         xmlns="http://www.w3.org/2000/svg"
  //         width="24"
  //         height="24"
  //         viewBox="0 0 24 24"
  //         fill="none"
  //       >
  //         <path
  //           d="M20 21C20 19.6044 20 18.9067 19.8278 18.3389C19.44 17.0605 18.4395 16.06 17.1611 15.6722C16.5934 15.5 15.8956 15.5 14.5 15.5H9.50001C8.10444 15.5 7.40666 15.5 6.83886 15.6722C5.56046 16.06 4.56004 17.0605 4.17224 18.3389C4 18.9067 4 19.6044 4 21M16.5 7.5C16.5 9.98528 14.4853 12 12 12C9.51472 12 7.5 9.98528 7.5 7.5C7.5 5.01472 9.51472 3 12 3C14.4853 3 16.5 5.01472 16.5 7.5Z"
  //           stroke="#475467"
  //           stroke-width="2"
  //           stroke-linecap="round"
  //           stroke-linejoin="round"
  //         />
  //       </svg>
  //     </div>

  //     <p className="text-gray-600 text-sm font-semibold">Business Logo</p>
  //   </div>

  //   <div className="grid grid-cols-2 gap-5 max-w-[250px] md:max-w-full">
  //     <Button
  //       outline={true}
  //       icon={
  //         <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
  //           <path
  //             d="M13.5 17.5H5.77614C5.2713 17.5 5.01887 17.5 4.90199 17.4002C4.80056 17.3135 4.74674 17.1836 4.75721 17.0506C4.76927 16.8974 4.94776 16.7189 5.30474 16.3619L12.3905 9.27614C12.7205 8.94613 12.8855 8.78112 13.0758 8.7193C13.2432 8.66492 13.4235 8.66492 13.5908 8.7193C13.7811 8.78112 13.9461 8.94613 14.2761 9.27614L17.5 12.5V13.5M13.5 17.5C14.9001 17.5 15.6002 17.5 16.135 17.2275C16.6054 16.9878 16.9878 16.6054 17.2275 16.135C17.5 15.6002 17.5 14.9001 17.5 13.5M13.5 17.5H6.5C5.09987 17.5 4.3998 17.5 3.86502 17.2275C3.39462 16.9878 3.01217 16.6054 2.77248 16.135C2.5 15.6002 2.5 14.9001 2.5 13.5V6.5C2.5 5.09987 2.5 4.3998 2.77248 3.86502C3.01217 3.39462 3.39462 3.01217 3.86502 2.77248C4.3998 2.5 5.09987 2.5 6.5 2.5H13.5C14.9001 2.5 15.6002 2.5 16.135 2.77248C16.6054 3.01217 16.9878 3.39462 17.2275 3.86502C17.5 4.3998 17.5 5.09987 17.5 6.5V13.5M8.75 7.08333C8.75 8.00381 8.00381 8.75 7.08333 8.75C6.16286 8.75 5.41667 8.00381 5.41667 7.08333C5.41667 6.16286 6.16286 5.41667 7.08333 5.41667C8.00381 5.41667 8.75 6.16286 8.75 7.08333Z"
  //             stroke="#9E6612"
  //             stroke-width="1.66667"
  //             stroke-linecap="round"
  //             stroke-linejoin="round"
  //           />
  //         </svg>
  //       }
  //     >
  //       Upload
  //     </Button>
  //   </div>
  // </div>
  //   );
}
