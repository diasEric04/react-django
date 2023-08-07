import { ReactElement } from 'react'
import { PostType } from '../contexts/PostContext/tsc-types'

export type Component = () => ReactElement
export type PostCardType = (state: PostType ) => ReactElement