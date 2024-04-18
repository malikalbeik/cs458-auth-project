'use client'

import { useSession } from 'next-auth/react';

export default function Home() {
  const { data: session } = useSession();

  return (
    <main>
      {session?.user ? (
        <div>
          <h1>Welcome, you are now signed in</h1>
          <p>Click <a href="https://github.com/ilkerozgen/cs458-project-3">here</a> to visit our deployed website.</p>
        </div>
      ) : (
        <h1>Loading...</h1>
      )}
    </main>
  );
}
