PGDMP                         {           data    15.3    15.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16398    data    DATABASE     w   CREATE DATABASE data WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'French_France.1252';
    DROP DATABASE data;
                postgres    false            �            1259    16418    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    fullname character varying(100) NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    email character varying(50) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16417    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    217            	           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    216            �            1259    16410    utilisateur    TABLE     �   CREATE TABLE public.utilisateur (
    id integer NOT NULL,
    nom character varying(300),
    prenom character varying(300),
    email character varying(400),
    mot_de_passe character varying(500),
    role_id integer DEFAULT 2
);
    DROP TABLE public.utilisateur;
       public         heap    postgres    false            �            1259    16409    utilisateur_id_seq    SEQUENCE     �   CREATE SEQUENCE public.utilisateur_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.utilisateur_id_seq;
       public          postgres    false    215            
           0    0    utilisateur_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.utilisateur_id_seq OWNED BY public.utilisateur.id;
          public          postgres    false    214            l           2604    16421    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    217    217            j           2604    16413    utilisateur id    DEFAULT     p   ALTER TABLE ONLY public.utilisateur ALTER COLUMN id SET DEFAULT nextval('public.utilisateur_id_seq'::regclass);
 =   ALTER TABLE public.utilisateur ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215                      0    16418    users 
   TABLE DATA           H   COPY public.users (id, fullname, username, password, email) FROM stdin;
    public          postgres    false    217   �                  0    16410    utilisateur 
   TABLE DATA           T   COPY public.utilisateur (id, nom, prenom, email, mot_de_passe, role_id) FROM stdin;
    public          postgres    false    215   �                  0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 1, false);
          public          postgres    false    216                       0    0    utilisateur_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.utilisateur_id_seq', 6, true);
          public          postgres    false    214            p           2606    16423    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    217            n           2606    16416    utilisateur utilisateur_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.utilisateur
    ADD CONSTRAINT utilisateur_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.utilisateur DROP CONSTRAINT utilisateur_pkey;
       public            postgres    false    215                  x������ � �          �  x����R[1���s�5#�&�U�4�0��C��L7�l')���	�w]t����Ɵd�%��s~Y��j8Ї�n��r5�OK1>�[��xs<3ӳ�z������%���Sєمd��U4��RL�j����ƈ�R` �X:��n����g8�M7翏�h��s���	T�+��J�U{ELR@o2�J�F�T�!aͬ�e&��u���Vÿ�>	_�����|�v�����՜���j��P�"���.QF�ꀊF�>��`�yA��6�햒V�s�c̿.�#�md{<n�ɺ�6`���Π�U�����b��b�BV0����I93$�,hc�n�]<|�>�ˎ�����u:�N������%T́�D3��P�`�یD�a#Y�=�4�2;;	�v\�'����g;=1�����|X�������R!S�����1�D�=C_c%A�ڰD��y:3�u0�L���     