import { usePage } from '@inertiajs/react';

function Modal({ modal, props }) {
  return modal({ ...props });
}

// To add Alerts
// <div className={`ease-transition ${sidebarShrinked ? `lg:pl-[70px]` : `lg:pl-72`}`}>
//   {props?.messages?.map((message) => (
//     <Alert key={message.id} description={message.message} type={message.level} />
//   ))}

//   <main>
//     <div>{children}</div>
//   </main>
// </div>;

export default function LayoutWrapper({ children }) {
  const { props, extras, url } = usePage();
  let modal = null;
  if (extras?.modal)
    modal = import.meta.glob('../pages/**/*.jsx', { eager: true })[`../pages/${extras.modal}.jsx`].default;

  return (
    <>
      {modal && <Modal key={url} modal={modal} props={props} />}
      {children}
    </>
  );
}
