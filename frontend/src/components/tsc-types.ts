import { ReactElement } from 'react'

export type Component = () => ReactElement
export type PostCardType = (state: { title: string, description: string, author: string, content: string} ) => ReactElement