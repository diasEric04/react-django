import { ReactElement, ReactNode, Dispatch } from 'react'

interface PostType {
    title: string
    description: string
    author: string
    content: string
}
export interface ActionType {
    type: string,
}

export interface StateType {
    posts: PostType[]
    loading: boolean
}

export interface FactoryActionsType {
    [key:string] : () => void
}

export interface ContextType {
    postState : StateType
    actions: FactoryActionsType
}


export type DispatchType = Dispatch<ActionType>
export type BuildActionsType = (dispatch : DispatchType ) => FactoryActionsType
export type ContextProviderType = (props : {children : ReactNode}) => ReactElement
export type ReducerType = (state: StateType, action: ActionType) => StateType