import type { NextAuthOptions } from "next-auth"
import GitHubProvider from "next-auth/providers/github"
import FacebookProvider from "next-auth/providers/facebook"
import GoogleProvider from "next-auth/providers/google";

import CredentialsProvider from "next-auth/providers/credentials"


export const options: NextAuthOptions = {
    providers: [
        GitHubProvider({
            clientId: process.env.GITHUB_ID as string,
            clientSecret: process.env.GITHUB_SECRET as string,
        }),
        FacebookProvider({
            clientId: process.env.FACEBOOK_CLIENT_ID as string,
            clientSecret: process.env.FACEBOOK_CLIENT_SECRE as string,
        }),
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID as string,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET as string
        }),
        CredentialsProvider({
            name: "Credentials",
            credentials: {
                email: { label: "email:", type: "email", placeholder: "example@email.com" },
                phone_number: { label: "phone number:", type: "text", placeholder: "05555555555" },
                password: { label: "Password:", type: "password" },
            },
            async authorize(credentials) {
                const user = {
                    id: 1, email: "test_user@gmail.com", phone_number: "05555555556", password: "test_password"
                }

                if ((credentials?.email === user.email || credentials?.phone_number === user.phone_number) && credentials?.password === user.password) {
                    return user as any
                } else {
                    return null
                }
            }
        })
    ],
}
