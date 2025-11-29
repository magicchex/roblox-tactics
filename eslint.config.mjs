import { defineConfig, globalIgnores } from "eslint/config";
import robloxTs from "eslint-plugin-roblox-ts";
import typescriptEslintEslintPlugin from "@typescript-eslint/eslint-plugin";
import prettier from "eslint-plugin-prettier";
import tsParser from "@typescript-eslint/parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
	baseDirectory: __dirname,
	recommendedConfig: js.configs.recommended,
	allConfig: js.configs.all
});

export default defineConfig([
	globalIgnores(["build/**", "out/**", "node_modules/**", "include/**", "eslint.config.mjs", "**/**Asphalt**"]),
	{
		extends: compat.extends(
			"eslint:recommended",
			"plugin:@typescript-eslint/recommended",
			"plugin:prettier/recommended",
			"plugin:roblox-ts/recommended-legacy"
		),

		plugins: {
			"@typescript-eslint": typescriptEslintEslintPlugin,
			prettier
		},

		languageOptions: {
			parser: tsParser,
			ecmaVersion: 2018,
			sourceType: "module",

			parserOptions: {
				jsx: true,
				useJSXTextNode: true,
				project: "./tsconfig.json"
			}
		},

		rules: {
			"prettier/prettier": "warn",

			"@typescript-eslint/array-type": [
				"warn",
				{
					default: "generic",
					readonly: "generic"
				}
			],

			"@typescript-eslint/no-unused-vars": "warn",
			"@typescript-eslint/explicit-function-return-type": "warn",
			"@typescript-eslint/no-namespace": "warn",
			"@typescript-eslint/no-non-null-assertion": "off",
			"@typescript-eslint/no-empty-function": "warn",

			"prefer-const": [
				"warn",
				{
					destructuring: "all"
				}
			],

			"no-undef-init": "error",
			"no-mixed-spaces-and-tabs": "error",
			"constructor-super": "error"
		}
	}
]);
