-- ========================================================================
-- THEARA COLOR — Supabase PostgreSQL Schema & Row Level Security (RLS)
-- Founder: Krai Theara | "Create Your Look"
-- ========================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. PROFILES (Extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- 2. CREDITS & SUBSCRIPTIONS
CREATE TYPE plan_tier_enum AS ENUM ('free', 'creator', 'pro', 'studio');

CREATE TABLE IF NOT EXISTS public.subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    plan_tier plan_tier_enum NOT NULL DEFAULT 'free',
    status TEXT NOT NULL DEFAULT 'active', -- active, past_due, canceled
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    current_period_start TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()),
    current_period_end TIMESTAMPTZ DEFAULT (TIMEZONE('utc', NOW()) + INTERVAL '30 days'),
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS public.credits (
    user_id UUID PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
    balance INT NOT NULL DEFAULT 50 CHECK (balance >= 0),
    lifetime_used INT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

CREATE TYPE credit_action_enum AS ENUM (
    'generation',
    'reference_analysis',
    'export_cube',
    'export_xmp',
    'refund',
    'monthly_refill',
    'bonus'
);

CREATE TABLE IF NOT EXISTS public.credit_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    amount INT NOT NULL, -- negative for deduction, positive for refund/credit
    action credit_action_enum NOT NULL,
    reference_id UUID,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- 3. PROJECTS
CREATE TABLE IF NOT EXISTS public.projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    is_archived BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- 4. ASSETS (Originals & References)
CREATE TYPE asset_type_enum AS ENUM ('original', 'reference', 'preview');

CREATE TABLE IF NOT EXISTS public.assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES public.projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    asset_type asset_type_enum NOT NULL,
    storage_path TEXT NOT NULL,
    filename TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    file_size INT NOT NULL,
    width INT,
    height INT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- 5. LOOKS
CREATE TABLE IF NOT EXISTS public.looks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    prompt TEXT,
    parameters JSONB NOT NULL,
    look_dna JSONB NOT NULL,
    original_asset_id UUID REFERENCES public.assets(id) ON DELETE SET NULL,
    preview_url TEXT,
    is_public BOOLEAN NOT NULL DEFAULT FALSE,
    category TEXT DEFAULT 'Cinematic',
    downloads_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- 6. LOOK VERSIONS (History/Revisions)
CREATE TABLE IF NOT EXISTS public.look_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    look_id UUID NOT NULL REFERENCES public.looks(id) ON DELETE CASCADE,
    version_number INT NOT NULL,
    parameters JSONB NOT NULL,
    intensity FLOAT NOT NULL DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL,
    UNIQUE(look_id, version_number)
);

-- 7. GENERATIONS (Audit of every AI request)
CREATE TYPE generation_status_enum AS ENUM ('queued', 'processing', 'completed', 'failed');

CREATE TABLE IF NOT EXISTS public.generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    project_id UUID REFERENCES public.projects(id) ON DELETE SET NULL,
    prompt TEXT NOT NULL,
    reference_asset_id UUID REFERENCES public.assets(id) ON DELETE SET NULL,
    parameters_generated JSONB,
    look_dna JSONB,
    cost_credits INT NOT NULL DEFAULT 10,
    status generation_status_enum NOT NULL DEFAULT 'completed',
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- 8. EXPORTS (.cube and .xmp download files)
CREATE TYPE export_format_enum AS ENUM ('cube', 'xmp');

CREATE TABLE IF NOT EXISTS public.exports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    look_id UUID NOT NULL REFERENCES public.looks(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    format export_format_enum NOT NULL,
    lut_size INT DEFAULT 33,
    storage_path TEXT NOT NULL,
    download_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT TIMEZONE('utc', NOW()) NOT NULL
);

-- ========================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ========================================================================

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.credits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.credit_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.looks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.look_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.generations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.exports ENABLE ROW LEVEL SECURITY;

-- Profiles: Users can read and update their own profile
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Credits & Subscriptions: Read-only to users, updated by backend service key
CREATE POLICY "Users can view own credits" ON public.credits
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view own subscriptions" ON public.subscriptions
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view own credit transactions" ON public.credit_transactions
    FOR SELECT USING (auth.uid() = user_id);

-- Projects: CRUD for project owners
CREATE POLICY "Users manage own projects" ON public.projects
    FOR ALL USING (auth.uid() = user_id);

-- Assets: CRUD for asset owners
CREATE POLICY "Users manage own assets" ON public.assets
    FOR ALL USING (auth.uid() = user_id);

-- Looks: Owners can manage their looks; anyone can view public looks
CREATE POLICY "Users manage own looks" ON public.looks
    FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Anyone can view public looks" ON public.looks
    FOR SELECT USING (is_public = TRUE);

-- Look Versions: Owner can view/create versions
CREATE POLICY "Users manage own look versions" ON public.look_versions
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.looks
            WHERE looks.id = look_versions.look_id AND looks.user_id = auth.uid()
        )
    );

-- Generations: Owner can view generations
CREATE POLICY "Users view own generations" ON public.generations
    FOR SELECT USING (auth.uid() = user_id);

-- Exports: Owner can view and download exports
CREATE POLICY "Users manage own exports" ON public.exports
    FOR ALL USING (auth.uid() = user_id);

-- ========================================================================
-- ATOMIC CREDIT TRANSACTION FUNCTION (Prevents Race Conditions)
-- ========================================================================

CREATE OR REPLACE FUNCTION public.deduct_credits(
    p_user_id UUID,
    p_amount INT,
    p_action credit_action_enum,
    p_reference_id UUID DEFAULT NULL,
    p_description TEXT DEFAULT NULL
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_balance INT;
BEGIN
    -- Acquire exclusive row lock on user credit record
    SELECT balance INTO v_balance
    FROM public.credits
    WHERE user_id = p_user_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'User credit record not found';
    END IF;

    IF v_balance < p_amount THEN
        RETURN FALSE; -- Insufficient balance
    END IF;

    -- Deduct balance
    UPDATE public.credits
    SET balance = balance - p_amount,
        lifetime_used = lifetime_used + p_amount,
        updated_at = TIMEZONE('utc', NOW())
    WHERE user_id = p_user_id;

    -- Record transaction
    INSERT INTO public.credit_transactions (
        user_id,
        amount,
        action,
        reference_id,
        description
    ) VALUES (
        p_user_id,
        -p_amount,
        p_action,
        p_reference_id,
        p_description
    );

    RETURN TRUE;
END;
$$;

