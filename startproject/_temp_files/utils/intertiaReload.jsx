import { router } from '@inertiajs/react';

export default function intertiaReload(only) {
  setTimeout(() => {
    router.reload({
      only: only,
    });
  }, 0);
}
