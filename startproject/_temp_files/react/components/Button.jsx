import { Link } from '@inertiajs/react';

const BUTTON_SIZES = {
  xs: 'h-6 px-[8px] text-xs',
  small: 'h-8 px-[10px]',
  medium: 'py-1.5 md:py-2.0',
  large: 'py-3 md:py-3.5',
};

export default function Button({
  children,
  className,
  loading,
  disabled,
  block = true,
  outline,
  typeColor,
  size = 'medium',
  buttonType = 'button',
  ...props
}) {
  const buttonStyle = () => {
    if (disabled)
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md border border-gray-300 bg-gray-100 px-3 text-sm font-semibold leading-6 text-gray-400 shadow-sm cursor-not-allowed ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'gray')
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md border border-gray-300 bg-gray-100 px-3 text-sm font-semibold leading-6 text-gray-800 shadow-sm hover:bg-gray-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-yellow-600 active:bg-gray-300 transition-all ease-in-out duration-100 ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'red')
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md border border-red-600 bg-red-600 px-3 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-red-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600 active:bg-red-300 transition-all ease-in-out duration-100 ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'transparent')
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md border border-gray-300 bg-transparent px-3 text-sm font-semibold leading-6 text-gray-900 shadow-sm hover:bg-gray-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-yellow-600 active:bg-gray-300 transition-all ease-in-out duration-100 ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'danger')
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md bg-red-600 px-3 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600 active:bg-red-300 transition-all ease-in-out duration-100 ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'link')
      return `flex justify-center items-center whitespace-nowrap gap-1 px-3 text-sm text-brand-500 hover:text-brand-600 font-semibold  ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'yellow')
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md border border-yellow-600 bg-yellow-600 px-3 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-yellow-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-yellow-600 active:bg-yellow-300 transition-all ease-in-out duration-100 ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    if (typeColor === 'white')
      return `flex justify-center items-center whitespace-nowrap gap-1 rounded-md border border-gray-300 bg-white px-3 text-sm font-semibold leading-6 text-gray-800 shadow-sm hover:bg-gray-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-yellow-600 active:bg-gray-300 transition-all ease-in-out duration-100 ${
        block ? 'w-full' : 'w-auto'
      } ${BUTTON_SIZES[size]}`;
    return `flex justify-center whitespace-nowrap items-center gap-1 rounded-md bg-brand-600 px-3 text-sm font-semibold leading-6 shadow-sm hover:bg-brand-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-700 ${
      block ? 'w-full' : 'w-auto'
    } ${BUTTON_SIZES[size]} ${
      outline ? 'bg-transparent border border-brand-600 text-brand-600 hover:text-white transition-none' : 'text-white'
    }`;
  };

  if (buttonType == 'a')
    return (
      <a {...props} className={`${className || ''} ${buttonStyle()}`} disabled={disabled || loading}>
        {loading ? (
          <svg
            aria-hidden="true"
            role="status"
            className="inline mr-3 w-4 h-4 text-white animate-spin"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="#E5E7EB"
            ></path>
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentColor"
            ></path>
          </svg>
        ) : (
          props.icon
        )}
        {children}
      </a>
    );
  if (buttonType == 'link')
    return (
      <Link {...props} className={`${className || ''} ${buttonStyle()}`} disabled={disabled || loading}>
        {loading ? (
          <svg
            aria-hidden="true"
            role="status"
            className="inline mr-3 w-4 h-4 text-white animate-spin"
            viewBox="0 0 100 101"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              fill="#E5E7EB"
            ></path>
            <path
              d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              fill="currentColor"
            ></path>
          </svg>
        ) : (
          props.icon
        )}
        {children}
      </Link>
    );

  return (
    <button {...props} className={`${className || ''} ${buttonStyle()}`} disabled={disabled || loading}>
      {loading ? (
        <svg
          aria-hidden="true"
          role="status"
          className="inline mr-3 w-4 h-4 text-white animate-spin"
          viewBox="0 0 100 101"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="#E5E7EB"
          ></path>
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentColor"
          ></path>
        </svg>
      ) : (
        props.icon
      )}
      {children}
    </button>
  );
}
