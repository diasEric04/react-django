import { ReactElement, ReactNode, Dispatch } from 'react'

export interface PostType {
    title: string
    description: string
    created_by: string
    updated_by: string
    updated_at: string
    created_at: string
    content: string
}
export interface ActionType {
    type: string,
    payload? : PostType[] | undefined
}

export interface StateType {
    posts: PostType[]
    loading: boolean
}

export interface FactoryActionsType {
    [key:string] : (post? : PostType[]) => void
}

export interface ContextType {
    postState : StateType
    actions: FactoryActionsType
}


export type DispatchType = Dispatch<ActionType>
export type BuildActionsType = (dispatch : DispatchType ) => FactoryActionsType
export type ContextProviderType = (props : {children : ReactNode}) => ReactElement
export type ReducerType = (state: StateType, action: ActionType) => StateType