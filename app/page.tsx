'use client'

import { useSession } from 'next-auth/react';

export default function Home() {
  const { data: session } = useSession();

  return (
    <main>
      {session?.user ? (
        <div>
          <h1>Welcome, you are now signed in</h1>
          <p>Click <a href="https://ilkerozgen.github.io/cs458-project-3/">here</a> to go to Distance Calculator.</p>
        </div>
      ) : (
        <h1>Loading...</h1>
      )}
    </main>
  );
}
