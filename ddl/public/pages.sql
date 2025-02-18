create table pages
(
    id                 serial
        primary key,
    path               varchar(255)               not null,
    hash               varchar(255)               not null,
    title              varchar(255)               not null,
    description        varchar(255),
    "isPrivate"        boolean default false      not null,
    "isPublished"      boolean default false      not null,
    "privateNS"        varchar(255),
    "publishStartDate" varchar(255),
    "publishEndDate"   varchar(255),
    content            text,
    render             text,
    toc                json,
    "contentType"      varchar(255)               not null,
    "createdAt"        varchar(255)               not null,
    "updatedAt"        varchar(255)               not null,
    "editorKey"        varchar(255)
        constraint pages_editorkey_foreign
            references editors,
    "localeCode"       varchar(5)
        constraint pages_localecode_foreign
            references locales,
    "authorId"         integer
        constraint pages_authorid_foreign
            references users,
    "creatorId"        integer
        constraint pages_creatorid_foreign
            references users,
    extra              json    default '{}'::json not null
);

alter table pages
    owner to user2076c1e68a454bacb17c22eac613ed21;

