'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useSession } from 'next-auth/react';

export default function Home() {
  const { data: session } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (session?.user) {
      router.push('https://ilkerozgen.github.io/cs458-project-3/');
    }
  }, [session, router]);

  return (
    <main>
      <h1>Welcome, you are now signed in</h1>
    </main>
  );
}
