import { PostCardType } from "../tsc-types"

export const PostCard : PostCardType = ({ title, description, created_by, content}) => {
    return (
        <article>
            <h3>{title}</h3>
            <small>{description} <b><i>{created_by}</i></b></small>
            <hr />
            {content}
        </article>
    )
}