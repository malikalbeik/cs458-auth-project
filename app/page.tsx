'use client'

import Image from "next/image";
import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'


export default function Home() {
  const { data: session } = useSession({
    required: true,
    onUnauthenticated() {
      redirect('/api/auth/signin?callbackUrl=/')
    }
  })

  if (session?.user) {
    return (
      <main>
        <h1>Welcome you are now signed in</h1>
      </main>
    );
  }
}
