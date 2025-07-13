
CREATE TABLE public.clientes (
    id bigint NOT NULL,
    nome character varying(255) NOT NULL,
    email character varying(255) NOT NULL
);

ALTER TABLE public.clientes OWNER TO postgres;

CREATE SEQUENCE public.clientes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.clientes_id_seq OWNER TO postgres;
ALTER SEQUENCE public.clientes_id_seq OWNED BY public.clientes.id;

CREATE TABLE public.favoritos (
    cliente_id bigint NOT NULL,
    produto_id integer NOT NULL,
    review character varying(500)
);

ALTER TABLE public.favoritos OWNER TO postgres;

CREATE TABLE public.produtos (
    id integer NOT NULL,
    titulo character varying(255) NOT NULL,
    imagem character varying(255) NOT NULL,
    preco numeric(10,2) NOT NULL
);

ALTER TABLE public.produtos OWNER TO postgres;

ALTER TABLE ONLY public.clientes ALTER COLUMN id SET DEFAULT nextval('public.clientes_id_seq'::regclass);

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_email_key UNIQUE (email);

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.favoritos
    ADD CONSTRAINT favoritos_pkey PRIMARY KEY (cliente_id, produto_id);

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (id);

CREATE INDEX idx_clientes_email ON public.clientes USING btree (email);
CREATE INDEX idx_favoritos_cliente_id ON public.favoritos USING btree (cliente_id);
CREATE INDEX idx_favoritos_produto_id ON public.favoritos USING btree (produto_id);
CREATE INDEX idx_produtos_id ON public.produtos USING btree (id);

ALTER TABLE ONLY public.favoritos
    ADD CONSTRAINT fk_favoritos_cliente FOREIGN KEY (cliente_id) REFERENCES public.clientes(id) ON DELETE CASCADE;

ALTER TABLE ONLY public.favoritos
    ADD CONSTRAINT fk_favoritos_produto FOREIGN KEY (produto_id) REFERENCES public.produtos(id) ON DELETE CASCADE;
