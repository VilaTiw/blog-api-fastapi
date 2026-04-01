-- passwords:
-- admin → admin123
-- editor → editor123
-- user → user123

INSERT INTO users (username, email, role, hashed_password) VALUES
('admin', 'admin@test.com', 'ADMIN', '$2b$12$djh0Bn4gZxEDXKUm1PTlneagc1LrxvDt.sOyMQRcvKaAAQu9BczBK'),
('editor', 'editor@test.com', 'EDITOR', '$2b$12$MlXuLg6GwnPBB9qp7Dp8n.hU8ufiKtUwzdc7kO78PjvPzVe5XwEry'),
('user', 'user@test.com', 'USER', '$2b$12$fTKd6SfWv5Q9bhY5yoDXMezt1K9M.Y3dCG67iE9c1O0/thf5iWei6');

INSERT INTO articles (title, content, author_id) VALUES
('Breaking Bad', 'A chemistry teacher turned methamphetamine producer partners with a former student to build a drug empire.', 1),
('The Sopranos', 'A mob boss struggles to balance family life and his role as leader of a criminal organization.', 2),
('Dexter', 'A forensic expert leads a secret life as a vigilante serial killer targeting other criminals.', 3),
('Game of Thrones', 'Noble families fight for control over the lands of Westeros while an ancient enemy returns.', 1),
('Stranger Things', 'A group of kids uncover supernatural mysteries in a small town linked to a secret lab.', 2);