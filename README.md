# Sudoku Zero-Knowledge Proof Protocol

This project implements a cryptographic proof system for the solution of a 9x9 Sudoku puzzle, based on the protocol described in the research paper **"Cryptographic Proof Systems for Solutions of Sudoku Puzzles"**. The protocol is designed to demonstrate the validity of a Sudoku solution without revealing the actual solution, ensuring privacy for the prover. The protocol has a **2/3 soundness error** and communicates the proof efficiently with a complexity of **O(n² log n)**.

## Features
- **Zero-Knowledge Proof**: Proves the existence of a valid Sudoku solution without revealing it.
- **Commitment Scheme**: Uses cryptographic commitments to securely hide values during the verification process.
- **Efficiency**: The communication and computation complexity of the protocol is **O(n² log n)**, where n = 9 for a standard Sudoku grid.

## Protocol Overview
The core idea of the protocol is to triplicate each cell of the Sudoku grid, creating three versions for the row, column, and subgrid in which the cell participates. The prover commits to these values and must demonstrate the following properties to the verifier:
1. All values in the rows, columns, and subgrids are unique.
2. The three copies of each cell have the same value.
3. The predetermined filled-in cells contain the correct values.

The verifier then randomly chooses one of the following queries:
- **Query 1**: Verifies the uniqueness of values across rows, columns, and subgrids.
- **Query 2**: Verifies that each cell has the same value in its three occurrences.
- **Query 3**: Verifies that the filled-in cells contain the correct values.

If the prover can successfully answer all queries, the solution is valid, and the prover has demonstrated knowledge of the solution.


## Zero-Knowledge Property

The zero-knowledge property of the protocol ensures that the prover cannot learn anything beyond the fact that they know a valid solution to the Sudoku puzzle. Each query and its response are randomly generated, which ensures that no information about the solution is leaked during the interaction.

## Conclusion

This implementation of the Sudoku zero-knowledge proof protocol is efficient and ensures privacy for the prover. It is based on the protocol described in the referenced research paper, and the proof system can be adapted for other Sudoku grid sizes.

## Acknowledgments

- The protocol is based on the ideas presented in the research paper **"Cryptographic Proof Systems for Solutions of Sudoku Puzzles"**.
- The implementation was created to demonstrate cryptographic proof systems for Sudoku puzzles and is intended for educational and research purposes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
